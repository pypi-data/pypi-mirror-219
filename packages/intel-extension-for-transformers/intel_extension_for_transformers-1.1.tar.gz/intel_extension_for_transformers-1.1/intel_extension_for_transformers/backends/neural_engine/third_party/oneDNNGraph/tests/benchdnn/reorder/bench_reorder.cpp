/*******************************************************************************
* Copyright 2017-2022 Intel Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#include <string.h>

#include <sstream>

#include "dnnl_common.hpp"
#include "utils/parser.hpp"

#include "graph_reorder.hpp"
#include "reorder.hpp"

namespace reorder {

void check_correctness(const settings_t &s) {
    for_(const auto &i_sdt : s.sdt)
    for_(const auto &i_ddt : s.ddt)
    for_(const auto &i_stag : s.stag)
    for_(const auto &i_dtag : s.dtag)
    for_(const auto &i_oflag : s.oflag)
    for_(const auto &i_cross_engine : s.cross_engine)
    for_(const auto &i_oscale : s.oscale)
    for_(const auto &i_zero_points : s.zero_points)
    for_(const auto &i_post_ops : s.post_ops)
    for_(const auto &i_scratchpad_mode : s.scratchpad_mode)
    for (auto i_runtime_dim_mask : s.runtime_dim_mask) {
        if (i_oscale.policy == policy_t::PER_OC) {
            fprintf(stderr,
                    "ERROR: reorder driver: `per_oc` policy is not supported "
                    "due to potential ambiguity. Please use one of `per_dim_0` "
                    "or `per_dim_1` policies.\n"),
                    fflush(stderr);
            SAFE_V(FAIL);
        }
        if (i_cross_engine != NONE && is_cpu()) {
            fprintf(stderr,
                    "ERROR: reorder driver: `cpu` engine does not support "
                    "anything but `--cross-engine=none`.\n"),
                    fflush(stderr);
            SAFE_V(FAIL);
        }

        // Enable multiple scales in case user requested it via passing `0.f`
        // in output scale attributes.
        const std::vector<float> test_scales = i_oscale.scale == 0
                ? s.def_scale
                : std::vector<float>(1, i_oscale.scale);

        for (const auto &i_test_scale : test_scales) {
            const attr_t::scale_t test_oscale(
                    i_oscale.policy, i_test_scale, i_oscale.runtime);
            auto attr = settings_t::get_attr(
                    test_oscale, i_zero_points, i_post_ops, i_scratchpad_mode);

            const prb_t prb(s.prb_dims, i_sdt, i_ddt, i_stag, i_dtag, attr,
                    i_oflag, i_cross_engine, i_runtime_dim_mask);
            std::stringstream ss;
            ss << prb;
            const std::string cpp_pstr = ss.str();
            const char *pstr = cpp_pstr.c_str();
            BENCHDNN_PRINT(1, "run: %s\n", pstr);

            res_t res {};
            if (api_mode == GRAPH)
                benchdnnext::reorder::doit(&prb, &res);
            else
                doit(&prb, &res);

            parse_result(res, pstr);

            if (is_bench_mode(PERF)) {
                perf_report_t pr(&prb, s.perf_template);
                pr.report(&res, pstr);
            }
        }
    }
}

static const std::string help_oflag
        = "FLAG:MASK[+...]    (Default: not specified)\n    Specifies `extra` "
          "field of destination memory descriptor.\n    `FLAG` values are "
          "`s8s8_comp` and `zp_comp`.\n    `MASK` is an non-negative integer "
          "specifying dimension to apply compensation.\n";

static const std::string help_runtime_dim_mask
        = "UINT    (Default: `0`)\n    Specifies a bit-mask that indicates "
          "whether a dimension is `DNNL_RUNTIME_DIM_VAL` if `1` on a "
          "correspondent dimension.\n";

static const std::string help_def_scales
        = "FLOAT\n    Output scales, used to improve testing coverage.\n    If "
          "`--attr-oscale` is specified, does not have an effect.\n";

static const std::string help_cross_engine
        = "KIND    (Default: `none`)\n    Specifies `KIND` of cross-engine "
          "used for benchmarking.\n    `KIND` values are `none`, `cpu2gpu` or "
          "`gpu2cpu`.\n";

int bench(int argc, char **argv) {
    driver_name = "reorder";
    using namespace parser;
    static settings_t s;
    static const settings_t def {};
    for (; argc > 0; --argc, ++argv) {
        const bool parsed_options = parse_bench_settings(argv[0])
                || parse_batch(bench, argv[0])
                || parse_dt(s.sdt, def.sdt, argv[0], "sdt")
                || parse_dt(s.ddt, def.ddt, argv[0], "ddt")
                || parse_tag(s.stag, def.stag, argv[0], "stag")
                || parse_tag(s.dtag, def.dtag, argv[0], "dtag")
                || parse_multivector_option(s.oflag, def.oflag, str2flag,
                        argv[0], "oflag", help_oflag, ',', '+')
                || parse_vector_option(s.runtime_dim_mask, def.runtime_dim_mask,
                        atoi, argv[0], "runtime-dim-mask",
                        help_runtime_dim_mask)
                || parse_vector_option(s.def_scale, def.def_scale, atof,
                        argv[0], "def-scales", help_def_scales)
                || parse_vector_option(s.cross_engine, def.cross_engine,
                        str2cross_engine, argv[0], "cross-engine",
                        help_cross_engine)
                || parse_attr_oscale(s.oscale, argv[0])
                || parse_attr_zero_points(s.zero_points, argv[0])
                || parse_attr_post_ops(s.post_ops, argv[0])
                || parse_attr_scratchpad_mode(
                        s.scratchpad_mode, def.scratchpad_mode, argv[0])
                || parse_perf_template(s.perf_template, s.perf_template_def,
                        s.perf_template_csv(), argv[0])
                || parse_reset(s, argv[0]) || parse_help(argv[0]);
        if (!parsed_options) {
            catch_unknown_options(argv[0]);

            parse_prb_dims(s.prb_dims, argv[0]);
            check_correctness(s);
        }
    }

    return parse_last_argument();
}

} // namespace reorder
