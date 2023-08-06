/*******************************************************************************
* Copyright 2022-2023 Intel Corporation
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

#ifndef UTILS_SETTINGS_HPP
#define UTILS_SETTINGS_HPP

struct base_settings_t {
    base_settings_t() {
        dnnl_get_default_fpmath_mode(&(this->fpmath_mode[0]));
    };

    std::vector<int64_t> mb {0};
    std::vector<bool> inplace {false};
    std::vector<attr_t::scale_t> oscale {attr_t::scale_t()};
    std::vector<attr_t::arg_scales_t> scales {attr_t::arg_scales_t()};
    std::vector<attr_t::zero_points_t> zero_points {attr_t::zero_points_t()};
    std::vector<attr_t::post_ops_t> post_ops {attr_t::post_ops_t()};
    std::vector<dnnl_scratchpad_mode_t> scratchpad_mode {
            dnnl_scratchpad_mode_library};
    std::vector<dnnl_fpmath_mode_t> fpmath_mode {dnnl_fpmath_mode_strict};
    const char *pattern = NULL;

    const char *perf_template_csv_base(const std::string &driver_args) const {
        static const std::string csv_pre
                = std::string("perf,%engine%,%impl%,%name%,");
        static const std::string csv_post = std::string(
                ",%attr%,%DESC%,%Gops%,%-time%,%-Gflops%,%0time%,%0Gflops%");
        static const std::string csv = csv_pre + driver_args + csv_post;
        return csv.c_str();
    }

    const char *perf_template_def
            = "perf,%engine%,%impl%,%name%,%prb%,%Gops%,%-time%,%-Gflops%,%"
              "0time%,%0Gflops%";
    const char *perf_template = perf_template_def;

    template <typename... ArgsT>
    static attr_t get_attr(const ArgsT &...args) {
        attr_t attr;
        attr.insert(args...);
        return attr;
    }
};

#endif
