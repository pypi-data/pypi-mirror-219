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

#include <stdlib.h>
#include <string.h>

#include "common.hpp"
#include "dnnl_common.hpp"
#include "dnnl_memory.hpp"
#include "utils/parser.hpp"

#include "self/self.hpp"

using namespace parser;

namespace self {

using pk_t = attr_t::post_ops_t::kind_t;

static int check_simple_enums() {
    /* attr::post_ops::kind */
    using p = attr_t::post_ops_t;
    SELF_CHECK_CASE_STR_EQ(p::kind2str(p::kind_t::SUM), "sum");
    SELF_CHECK_CASE_STR_EQ(p::kind2str(p::kind_t::RELU), "relu");

    SELF_CHECK_EQ(p::str2kind("sum"), p::kind_t::SUM);
    SELF_CHECK_EQ(p::str2kind("SuM"), p::kind_t::SUM);

    SELF_CHECK_EQ(p::str2kind("relu"), p::kind_t::RELU);
    SELF_CHECK_EQ(p::str2kind("ReLU"), p::kind_t::RELU);

    return OK;
}

static int check_attr2str() {
    attr_t attr;
    SELF_CHECK_EQ(attr.is_def(), true);

    SELF_CHECK_PRINT_EQ(attr, "");

    attr.oscale.policy = policy_t::COMMON;
    attr.oscale.scale = 2.4;
    SELF_CHECK_PRINT_EQ(attr, "--attr-oscale=common:2.4 ");

    attr.oscale.policy = policy_t::PER_OC;
    attr.oscale.scale = 3.2;
    attr.oscale.runtime = true;
    SELF_CHECK_PRINT_EQ(attr, "--attr-oscale=per_oc:3.2* ");

    attr.oscale.policy = policy_t::PER_DIM_01;
    attr.oscale.scale = 3.2;
    attr.oscale.runtime = false;
    SELF_CHECK_PRINT_EQ(attr, "--attr-oscale=per_dim_01:3.2 ");

    attr.zero_points.set(DNNL_ARG_SRC, policy_t::COMMON, 1, false);
    SELF_CHECK_PRINT_EQ(attr,
            "--attr-oscale=per_dim_01:3.2 --attr-zero-points=src:common:1 ");

    attr.zero_points.set(DNNL_ARG_SRC, policy_t::PER_DIM_0, 3, false);
    attr.zero_points.set(DNNL_ARG_WEIGHTS, {policy_t::PER_DIM_1, 2, true});
    SELF_CHECK_PRINT_EQ2(attr,
            "--attr-oscale=per_dim_01:3.2 "
            "--attr-zero-points=src:per_dim_0:3+wei:per_dim_1:2* ",
            "--attr-oscale=per_dim_01:3.2 "
            "--attr-zero-points=wei:per_dim_1:2*+src:per_dim_0:3 ");

    attr = attr_t();
    attr.scales.set(DNNL_ARG_SRC_0, attr_t::scale_t(policy_t::COMMON, 2.3));
    SELF_CHECK_PRINT_EQ(attr, "--attr-scales=src:common:2.3 ");

    attr = attr_t();
    attr.scales.set(
            DNNL_ARG_SRC_0, attr_t::scale_t(policy_t::COMMON, 2.3, true));
    SELF_CHECK_PRINT_EQ(attr, "--attr-scales=src:common:2.3* ");

    attr.scales.set(DNNL_ARG_SRC_0, attr_t::scale_t(policy_t::COMMON, 2.2));
    attr.scales.set(DNNL_ARG_SRC_1, attr_t::scale_t(policy_t::COMMON, 3));
    SELF_CHECK_PRINT_EQ(attr, "--attr-scales=src:common:2.2+src1:common:3 ");

    return OK;
}

static int check_attr() {
#define SELF_CHECK_OSCALE(os, os_policy, os_scale, os_runtime) \
    do { \
        SELF_CHECK_EQ((os).policy, policy_t::os_policy); \
        SELF_CHECK_EQ((os).scale, os_scale); \
        SELF_CHECK_EQ((os).runtime, os_runtime); \
    } while (0)

#define SELF_CHECK_ATTR_OSCALE(str, os_policy, os_scale, os_runtime) \
    do { \
        std::vector<attr_t::scale_t> os; \
        SELF_CHECK_EQ(parse_attr_oscale(os, str), true); \
        SELF_CHECK_EQ(os.size(), 1); \
        SELF_CHECK_OSCALE(os[0], os_policy, os_scale, os_runtime); \
    } while (0)
#define SELF_CHECK_ATTR_ZP(zp, arg, zero_points_value, zero_points_runtime) \
    do { \
        const auto &entry = (zp).get(arg); \
        SELF_CHECK_EQ(entry.value, zero_points_value); \
        SELF_CHECK_EQ(entry.runtime, zero_points_runtime); \
    } while (0)

    SELF_CHECK_ATTR_OSCALE("--attr-oscale=", COMMON, 1., false);
    SELF_CHECK_ATTR_OSCALE("--attr-oscale=common:1.0", COMMON, 1., false);
    SELF_CHECK_ATTR_OSCALE("--attr-oscale=common:2.0", COMMON, 2., false);
    SELF_CHECK_ATTR_OSCALE("--attr-oscale=common:2.0*", COMMON, 2., true);
    SELF_CHECK_ATTR_OSCALE("--attr-oscale=per_oc:.5*", PER_OC, .5, true);

    {
        std::vector<attr_t::zero_points_t> zp;
        SELF_CHECK_EQ(parse_attr_zero_points(zp,
                              "--attr-zero-points=src:common:0+dst:common:-2*"),
                true);
        SELF_CHECK_EQ(zp.size(), 1);
        SELF_CHECK_ATTR_ZP(zp[0], DNNL_ARG_SRC, 0, false);
        SELF_CHECK_ATTR_ZP(zp[0], DNNL_ARG_WEIGHTS, 0, false);
        SELF_CHECK_ATTR_ZP(zp[0], DNNL_ARG_DST, -2, true);
    }

    {
        std::vector<attr_t::arg_scales_t> sc;
        SELF_CHECK_EQ(
                parse_attr_scales(sc, "--attr-scales=src1:common:1.5"), true);
        SELF_CHECK_EQ(sc.size(), 1);
        SELF_CHECK_EQ(sc[0].get(DNNL_ARG_SRC_1).policy, policy_t::COMMON);
        SELF_CHECK_EQ(sc[0].get(DNNL_ARG_SRC_1).scale, 1.5);
    }

    {
        std::vector<attr_t::arg_scales_t> sc;
        SELF_CHECK_EQ(parse_attr_scales(sc,
                              "--attr-scales=src:common:2.5+src1:common:1.5"),
                true);
        SELF_CHECK_EQ(sc.size(), 1);
        SELF_CHECK_EQ(sc[0].get(DNNL_ARG_SRC_0).policy, policy_t::COMMON);
        SELF_CHECK_EQ(sc[0].get(DNNL_ARG_SRC_0).scale, 2.5);
        SELF_CHECK_EQ(sc[0].get(DNNL_ARG_SRC_1).policy, policy_t::COMMON);
        SELF_CHECK_EQ(sc[0].get(DNNL_ARG_SRC_1).scale, 1.5);
    }

    // depthwise conv section
    {
        std::vector<attr_t::post_ops_t> po;
        auto st = parse_attr_post_ops(po, "--attr-post-ops=dw_k3s1p1");
        SELF_CHECK_EQ(st, true);
        SELF_CHECK_EQ(po[0].len(), 1);
        const auto &e = po[0].entry[0];
        SELF_CHECK_EQ(e.kind, pk_t::DW_K3S1P1);
        const auto &ce = e.convolution;
        SELF_CHECK_EQ(ce.stride, 1);
        SELF_CHECK_EQ(ce.dst_dt, dnnl_f32);
        SELF_CHECK_OSCALE(ce.oscale, COMMON, 1.f, false);
    }

    {
        std::vector<attr_t::post_ops_t> po;
        auto st = parse_attr_post_ops(po,
                "--attr-post-ops=relu:0.5+dw_k3s2p1:s8:per_oc:2+linear:2:1:3");
        SELF_CHECK_EQ(st, true);
        SELF_CHECK_EQ(po[0].len(), 3);
        auto &e = po[0].entry[0];
        SELF_CHECK_EQ(e.kind, pk_t::RELU);
        auto &ee = e.eltwise;
        SELF_CHECK_EQ(ee.alg, dnnl_eltwise_relu);
        SELF_CHECK_EQ(ee.alpha, 0.5f);
        SELF_CHECK_EQ(ee.beta, 0.f);
        SELF_CHECK_EQ(ee.scale, 1.f);

        e = po[0].entry[1];
        SELF_CHECK_EQ(e.kind, pk_t::DW_K3S2P1);
        const auto &ce = e.convolution;
        SELF_CHECK_EQ(ce.stride, 2);
        SELF_CHECK_EQ(ce.dst_dt, dnnl_s8);
        SELF_CHECK_OSCALE(ce.oscale, PER_OC, 2.f, false);

        e = po[0].entry[2];
        SELF_CHECK_EQ(e.kind, pk_t::LINEAR);
        ee = e.eltwise;
        SELF_CHECK_EQ(ee.alg, dnnl_eltwise_linear);
        SELF_CHECK_EQ(ee.alpha, 2.f);
        SELF_CHECK_EQ(ee.beta, 1.f);
        SELF_CHECK_EQ(ee.scale, 3.f);
    }

#undef SELF_CHECK_OSCALE
#undef SELF_CHECK_ATTR_OSCALE
#undef SELF_CHECK_ATTR_ZP

    return OK;
}

void append_sum(attr_t::post_ops_t &po, float ascale = 1.f,
        int32_t zero_point = 0, dnnl_data_type_t adt = dnnl_data_type_undef) {
    attr_t::post_ops_t::entry_t e(pk_t::SUM);
    e.sum.scale = ascale;
    e.sum.zero_point = zero_point;
    e.sum.dt = adt;
    po.entry.push_back(e);
}

void append_convolution(attr_t::post_ops_t &po, pk_t akind,
        dnnl_data_type_t adst_dt = dnnl_f32,
        policy_t apolicy = policy_t::COMMON, float ascale = 1.f) {
    attr_t::post_ops_t::entry_t e(akind);
    e.convolution.stride = e.kind == pk_t::DW_K3S1P1 ? 1 : 2;
    e.convolution.dst_dt = adst_dt;
    e.convolution.oscale = attr_t::scale_t(apolicy, ascale);
    po.entry.push_back(e);
}

void append_eltwise(attr_t::post_ops_t &po, pk_t akind, float aalpha = 0.f,
        float abeta = 0.f, float ascale = 1.f) {
    attr_t::post_ops_t::entry_t e(akind);
    e.eltwise.alg = attr_t::post_ops_t::kind2dnnl_kind(akind);
    e.eltwise.alpha = aalpha;
    e.eltwise.beta = abeta;
    e.eltwise.scale = ascale;
    po.entry.push_back(e);
}

static int check_post_ops2str() {
    attr_t::post_ops_t po;
    SELF_CHECK_EQ(po.is_def(), true);
    SELF_CHECK_PRINT_EQ(po, "");

    append_sum(po);
    SELF_CHECK_EQ(po.len(), 1);
    SELF_CHECK_PRINT_EQ(po, "sum");

    append_eltwise(po, pk_t::RELU);
    SELF_CHECK_EQ(po.len(), 2);
    SELF_CHECK_PRINT_EQ(po, "sum+relu");

    append_sum(po, 2.f, 1, dnnl_s8);
    SELF_CHECK_EQ(po.len(), 3);
    SELF_CHECK_PRINT_EQ(po, "sum+relu+sum:2:1:s8");

    append_eltwise(po, pk_t::LINEAR, 5.f, 10.f, 2.f);
    SELF_CHECK_EQ(po.len(), 4);
    SELF_CHECK_PRINT_EQ(po, "sum+relu+sum:2:1:s8+linear:5:10:2");

    append_convolution(po, pk_t::DW_K3S1P1);
    SELF_CHECK_EQ(po.len(), 5);
    SELF_CHECK_PRINT_EQ(po, "sum+relu+sum:2:1:s8+linear:5:10:2+dw_k3s1p1");

    append_convolution(po, pk_t::DW_K3S2P1, dnnl_s32, policy_t::PER_OC, 2.f);
    SELF_CHECK_EQ(po.len(), 6);
    SELF_CHECK_PRINT_EQ(po,
            "sum+relu+sum:2:1:s8+linear:5:10:2+dw_k3s1p1+dw_k3s2p1:s32:per_oc:"
            "2");

    return OK;
}

static int check_str2post_ops() {
    attr_t::post_ops_t ops;

    SELF_CHECK_EQ(ops.is_def(), true);

    auto quick = [&](int len) -> int {
        for (int i = 0; i < 2; ++i) {
            if (2 * i + 0 >= len) return OK;
            SELF_CHECK_EQ(ops.entry[2 * i + 0].kind, attr_t::post_ops_t::SUM);
            SELF_CHECK_EQ(ops.entry[2 * i + 0].sum.scale, 2. + i);
            if (2 * i + 1 >= len) return OK;
            SELF_CHECK_EQ(ops.entry[2 * i + 1].kind, attr_t::post_ops_t::RELU);
            SELF_CHECK_EQ(ops.entry[2 * i + 1].eltwise.scale, 1.);
            SELF_CHECK_EQ(ops.entry[2 * i + 1].eltwise.alpha, 0.);
            SELF_CHECK_EQ(ops.entry[2 * i + 1].eltwise.beta, 0.);
        }
        return OK;
    };

    ops.from_str("");
    SELF_CHECK_EQ(ops.is_def(), true);

    ops.from_str("sum:2");
    SELF_CHECK_EQ(quick(1), OK);

    ops.from_str("sum:2+relu");
    SELF_CHECK_EQ(quick(2), OK);

    ops.from_str("sum:2+relu+sum:3");
    SELF_CHECK_EQ(quick(3), OK);

    ops.from_str("sum:2+relu+sum:3+relu");
    SELF_CHECK_EQ(quick(4), OK);

    return OK;
}

static int check_tags() {
    dnnl_memory_desc_t md_from_tag;
    dnnl_memory_desc_t md_from_str;

    dnnl_dims_t dims = {7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};
    for (int tag_ = dnnl_format_tag_undef; tag_ != dnnl_format_tag_last;
            tag_++) {
        dnnl_format_tag_t format_tag = (dnnl_format_tag_t)tag_;
        const char *str_tag = fmt_tag2str(format_tag);
        int ndims = 1;
        for (char c = (char)('a' + DNNL_MAX_NDIMS - 1); c >= 'a'; c--) {
            if (strchr(str_tag, c)) {
                ndims = c - 'a' + 1;
                break;
            }
        }

        md_from_str = dnn_mem_t::init_md(ndims, dims, dnnl_f32, str_tag);
        DNN_SAFE(dnnl_memory_desc_init_by_tag(
                         &md_from_tag, ndims, dims, dnnl_f32, format_tag),
                CRIT);
        int eq = dnnl_memory_desc_equal(&md_from_tag, &md_from_str);
        SELF_CHECK_EQ(eq, 1);
    }

    return OK;
}

static int check_trim_tags() {
    {
        std::string tag = "BA16a16b4a";
        std::string ndims_trimmed_tag = trim_tag(tag, 1);
        SELF_CHECK_EQ(true, ndims_trimmed_tag == "A16a4a");
    }
    {
        std::string tag = "BA16a16b4a";
        std::string masked_trimmed_tag = trim_tag_by_mask(tag, 2);
        SELF_CHECK_EQ(true, masked_trimmed_tag == "A16a");
    }
    {
        std::string tag = "abcd";
        std::string ndims_trimmed_tag = trim_tag(tag, 2);
        SELF_CHECK_EQ(true, ndims_trimmed_tag == "ab");
    }
    {
        std::string tag = "abcd";
        std::string masked_trimmed_tag = trim_tag_by_mask(tag, 10);
        SELF_CHECK_EQ(true, masked_trimmed_tag == "ab");
    }
    {
        std::string tag = "abcd";
        std::string masked_trimmed_tag = trim_tag_by_mask(tag, 12);
        SELF_CHECK_EQ(true, masked_trimmed_tag == "ab");
    }
    {
        std::string tag = "aBcd16b";
        std::string ndims_trimmed_tag = trim_tag(tag, 2);
        SELF_CHECK_EQ(true, ndims_trimmed_tag == "aB16b");
    }
    {
        std::string tag = "aBcd16b";
        std::string masked_trimmed_tag = trim_tag_by_mask(tag, 2);
        SELF_CHECK_EQ(true, masked_trimmed_tag == "A16a");
    }
    {
        std::string tag = "BA16a16b4a";
        std::string masked_trimmed_tag = trim_tag_by_mask(tag, 1);
        SELF_CHECK_EQ(true, masked_trimmed_tag == "A16a4a");
    }
    {
        std::string tag = "BADC2c16a8d16b4a";
        std::string masked_trimmed_tag = trim_tag_by_mask(tag, 14);
        SELF_CHECK_EQ(true, masked_trimmed_tag == "ACB2b8c16a");
    }

    return OK;
}

static int check_skip_impl() {
    skip_impl = "gemm";
    SELF_CHECK_EQ(true, maybe_skip("x64:gemm:jit"));

    skip_impl = "ref,x64:gemm";
    SELF_CHECK_EQ(true, maybe_skip("x64:gemm:jit"));

    skip_impl = "this,finds,nothing";
    SELF_CHECK_EQ(false, maybe_skip("x64:gemm:jit"));

    return OK;
}

void common() {
    RUN(check_simple_enums());
    RUN(check_attr2str());
    RUN(check_attr());
    RUN(check_post_ops2str());
    RUN(check_str2post_ops());
    RUN(check_tags());
    RUN(check_trim_tags());
    RUN(check_skip_impl());
}

} // namespace self
