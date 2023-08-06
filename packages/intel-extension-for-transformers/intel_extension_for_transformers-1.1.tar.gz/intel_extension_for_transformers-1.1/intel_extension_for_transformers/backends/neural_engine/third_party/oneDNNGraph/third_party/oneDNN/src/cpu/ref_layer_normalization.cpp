/*******************************************************************************
* Copyright 2019-2023 Intel Corporation
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

#include <assert.h>
#include <math.h>

#include "common/c_types_map.hpp"
#include "common/dnnl_thread.hpp"
#include "common/type_helpers.hpp"

#include "cpu/cpu_primitive.hpp"
#include "cpu/ref_io_helper.hpp"
#include "cpu/ref_layer_normalization.hpp"

namespace dnnl {
namespace impl {
namespace cpu {

status_t ref_layer_normalization_fwd_t::execute_forward(
        const exec_ctx_t &ctx) const {
    const auto use_ss = pd()->use_scaleshift();
    const auto use_scale = pd()->use_scale();
    const auto use_shift = pd()->use_shift();

    const memory_desc_wrapper src_d(pd()->src_md());
    const memory_desc_wrapper dst_d(pd()->dst_md());
    const memory_desc_wrapper stat_d(pd()->stat_md());
    const memory_desc_wrapper ss_d(pd()->weights_md());

    const size_t shift_off
            = use_ss && !ss_d.has_zero_dim() ? ss_d.off(1, 0) : 0;

    auto src = CTX_IN_MEM(const void *, DNNL_ARG_SRC);
    auto scale = CTX_IN_MEM(
            const float *, use_scale ? DNNL_ARG_SCALE : DNNL_ARG_SCALE_SHIFT);
    auto shift = use_shift ? CTX_IN_MEM(const float *, DNNL_ARG_SHIFT)
            : use_ss       ? &scale[shift_off]
                           : nullptr;
    auto mean = pd()->stats_are_src()
            ? const_cast<float *>(CTX_IN_MEM(const float *, DNNL_ARG_MEAN))
            : CTX_OUT_MEM(float *, DNNL_ARG_MEAN);
    auto variance = pd()->stats_are_src()
            ? const_cast<float *>(CTX_IN_MEM(const float *, DNNL_ARG_VARIANCE))
            : CTX_OUT_MEM(float *, DNNL_ARG_VARIANCE);
    auto dst = CTX_OUT_MEM(void *, DNNL_ARG_DST);

    DEFINE_SCALES_BUFFER(scales);

    const dim_t N = pd()->across_axis();
    const dim_t C = pd()->norm_axis();

    const float eps = pd()->desc()->layer_norm_epsilon;
    const bool save_stats = pd()->is_training();
    const bool calculate_stats = !pd()->stats_are_src();

    const auto ss_off = [&use_scale, &use_shift, &use_ss](
                                const memory_desc_wrapper &md, dim_t c) {
        dim_t offset = 0;
        if (use_ss) offset = md.off(0, c);
        if (use_scale || use_shift) offset = md.off(c);
        return offset;
    };

    /* fast return */
    if (this->pd()->has_zero_dim_memory()) {
        if (calculate_stats && save_stats) {
            for (dim_t n = 0; n < N; n++) {
                mean[n] = 0;
                variance[n] = 0;
            }
        }
        return status::success;
    }

    parallel_nd(N, [&](dim_t n) {
        const size_t s_off = stat_d.off_l(n);
        auto v_mean = calculate_stats ? 0 : mean[s_off];
        auto v_variance = calculate_stats ? 0 : variance[s_off];

        if (calculate_stats) {
            for (dim_t c = 0; c < C; ++c) {
                const auto s_off = src_d.off_l(n * C + c);
                float s = io::load_float_value(src_d.data_type(), src, s_off);
                v_mean += s;
            }
            v_mean /= C;

            for (dim_t c = 0; c < C; ++c) {
                const auto s_off = src_d.off_l(n * C + c);
                float s = io::load_float_value(src_d.data_type(), src, s_off);
                float m = s - v_mean;
                v_variance += m * m;
            }
            v_variance /= C;
        }

        float sqrt_variance = sqrtf(v_variance + eps);
        for (dim_t c = 0; c < C; ++c) {
            const float sm
                    = (scale ? scale[ss_off(ss_d, c)] : 1.f) / sqrt_variance;
            const float sv = shift ? shift[ss_off(ss_d, c)] : 0;
            const auto s_off = src_d.off_l(n * C + c);
            const auto d_off = dst_d.off_l(n * C + c);
            float s = io::load_float_value(src_d.data_type(), src, s_off);
            float d = sm * (s - v_mean) + sv;
            d *= scales[0];
            io::store_float_value(dst_d.data_type(), d, dst, d_off);
        }

        if (calculate_stats) {
            if (save_stats) {
                mean[s_off] = v_mean;
                variance[s_off] = v_variance;
            }
        }
    });
    return status::success;
}

status_t ref_layer_normalization_bwd_t::execute_backward(
        const exec_ctx_t &ctx) const {
    status_t status = status::success;

    const memory_desc_wrapper src_d(pd()->src_md());
    const memory_desc_wrapper stat_d(pd()->stat_md());
    const memory_desc_wrapper diff_src_d(pd()->diff_src_md());
    const memory_desc_wrapper diff_dst_d(pd()->diff_dst_md());
    const memory_desc_wrapper ss_d(pd()->weights_md());
    const memory_desc_wrapper diff_ss_d(pd()->diff_weights_md());

    const auto use_ss = pd()->use_scaleshift();
    const auto use_scale = pd()->use_scale();
    const auto use_shift = pd()->use_shift();

    auto src = CTX_IN_MEM(const void *, DNNL_ARG_SRC);
    auto mean = CTX_IN_MEM(const float *, DNNL_ARG_MEAN);
    auto variance = CTX_IN_MEM(const float *, DNNL_ARG_VARIANCE);
    auto diff_dst = CTX_IN_MEM(const void *, DNNL_ARG_DIFF_DST);
    auto scale = CTX_IN_MEM(
            float *, use_scale ? DNNL_ARG_SCALE : DNNL_ARG_SCALE_SHIFT);
    auto diff_src = CTX_OUT_CLEAN_MEM(void *, DNNL_ARG_DIFF_SRC, status);
    CHECK(status);

    const size_t diff_shift_off
            = use_ss && !diff_ss_d.has_zero_dim() ? diff_ss_d.off(1, 0) : 0;

    auto diff_scale = use_scale
            ? CTX_OUT_CLEAN_MEM(float *, DNNL_ARG_DIFF_SCALE, status)
            : use_ss
            ? CTX_OUT_CLEAN_MEM(float *, DNNL_ARG_DIFF_SCALE_SHIFT, status)
            : nullptr;
    CHECK(status);
    auto diff_shift = use_shift
            ? CTX_OUT_CLEAN_MEM(float *, DNNL_ARG_DIFF_SHIFT, status)
            : use_ss ? &diff_scale[diff_shift_off]
                     : nullptr;
    CHECK(status);

    const dim_t N = pd()->across_axis();
    const dim_t C = pd()->norm_axis();

    const auto ss_off = [&use_scale, &use_shift, &use_ss](
                                const memory_desc_wrapper &md, dim_t c) {
        dim_t offset = 0;
        if (use_ss) offset = md.off(0, c);
        if (use_scale || use_shift) offset = md.off(c);
        return offset;
    };

    /* fast return */
    if (this->pd()->has_zero_dim_memory()) {
        if (diff_scale) {
            for (dim_t c = 0; c < C; ++c) {
                diff_scale[ss_off(diff_ss_d, c)] = 0;
            }
        }
        if (diff_shift) {
            for (dim_t c = 0; c < C; ++c) {
                diff_shift[ss_off(diff_ss_d, c)] = 0;
            }
        }
        return status::success;
    }

    const float eps = pd()->desc()->layer_norm_epsilon;
    const bool calculate_diff_stats = !pd()->use_global_stats();

    if (diff_scale || diff_shift) {
        parallel_nd(C, [&](dim_t c) {
            float diff_gamma = 0.f;
            float diff_beta = 0.f;

            for (dim_t n = 0; n < N; ++n) {
                const auto src_off = src_d.off_l(n * C + c);
                const auto diff_dst_off = diff_dst_d.off_l(n * C + c);
                const auto stat_off = stat_d.off_l(n);
                float inv_sqrt_variance = 1.f / sqrtf(variance[stat_off] + eps);
                float s = io::load_float_value(src_d.data_type(), src, src_off);
                float dd = io::load_float_value(
                        diff_dst_d.data_type(), diff_dst, diff_dst_off);
                diff_gamma += (s - mean[stat_off]) * dd * inv_sqrt_variance;
                diff_beta += dd;
            }

            if (diff_scale) diff_scale[ss_off(diff_ss_d, c)] = diff_gamma;
            if (diff_shift) diff_shift[ss_off(diff_ss_d, c)] = diff_beta;
        });
    }

    parallel_nd(N, [&](dim_t n) {
        const size_t s_off = stat_d.off_l(n);
        float inv_sqrt_variance = 1.f / sqrtf(variance[s_off] + eps);
        float dd_gamma = 0.f;
        float dd_gamma_x = 0.f;
        if (calculate_diff_stats) {
            for (dim_t c = 0; c < C; ++c) {
                float gamma = scale ? scale[ss_off(ss_d, c)] : 1.f;
                const auto src_off = src_d.off_l(n * C + c);
                const auto diff_dst_off = diff_dst_d.off_l(n * C + c);
                float s = io::load_float_value(src_d.data_type(), src, src_off);
                float dd = io::load_float_value(
                        diff_dst_d.data_type(), diff_dst, diff_dst_off);
                dd_gamma += dd * gamma;
                dd_gamma_x += dd * gamma * (s - mean[s_off]);
            }
            dd_gamma_x *= inv_sqrt_variance;
        }

        for (dim_t c = 0; c < C; ++c) {
            float gamma = scale ? scale[ss_off(ss_d, c)] : 1;
            const auto src_off = src_d.off_l(n * C + c);
            const auto diff_dst_off = diff_dst_d.off_l(n * C + c);
            const auto diff_src_off = diff_src_d.off_l(n * C + c);
            float dd = io::load_float_value(
                    diff_dst_d.data_type(), diff_dst, diff_dst_off);
            float d_src = dd * gamma;
            if (calculate_diff_stats) {
                float s = io::load_float_value(src_d.data_type(), src, src_off);
                d_src -= dd_gamma / C;
                d_src -= (s - mean[s_off]) * dd_gamma_x * inv_sqrt_variance / C;
            }
            d_src *= inv_sqrt_variance;
            io::store_float_value(
                    diff_src_d.data_type(), d_src, diff_src, diff_src_off);
        }
    });
    return status::success;
}

} // namespace cpu
} // namespace impl
} // namespace dnnl

// vim: et ts=4 sw=4 cindent cino^=l0,\:0,N-s
