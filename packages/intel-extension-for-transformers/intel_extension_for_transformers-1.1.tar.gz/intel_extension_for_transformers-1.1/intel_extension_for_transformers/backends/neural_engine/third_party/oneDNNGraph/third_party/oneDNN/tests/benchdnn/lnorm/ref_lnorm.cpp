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

#include "utils/parallel.hpp"

#include "lnorm/lnorm.hpp"

namespace lnorm {

void compute_ref_fwd(const prb_t *prb, const args_t &args) {
    const dnn_mem_t &src = args.find(DNNL_ARG_SRC);
    const dnn_mem_t &mean = args.find(DNNL_ARG_MEAN);
    const dnn_mem_t &var = args.find(DNNL_ARG_VARIANCE);
    const dnn_mem_t &ss
            = args.find(prb->use_sc() ? DNNL_ARG_SCALE : DNNL_ARG_SCALE_SHIFT);
    const dnn_mem_t &sh = args.find(DNNL_ARG_SHIFT);
    const dnn_mem_t &dst = args.find(DNNL_ARG_DST);

    float *dst_ptr = (float *)dst;

    const bool use_ss = prb->use_ss();
    const bool use_sc = prb->use_sc();
    const bool use_sh = prb->use_sh();

    benchdnn_parallel_nd(prb->n, [&](int64_t n) {
        float smean = mean.get_elem(n);
        float svar = var.get_elem(n);
        float sqrt_var = sqrtf(svar + prb->eps);

        for (int64_t c = 0; c < prb->c; ++c) {
            float gamma = (use_ss || use_sc ? ss.get_elem(c) : 1.0f) / sqrt_var;
            float beta = use_ss ? ss.get_elem(prb->c + c)
                    : use_sh    ? sh.get_elem(c)
                                : 0;
            auto off = n * prb->c + c;
            float res = gamma * (src.get_elem(off) - smean) + beta;
            maybe_oscale(prb->attr, res, prb->scales, 0);
            dst_ptr[off] = res;
        }
    });
}

void compute_ref_bwd(const prb_t *prb, const args_t &args) {
    const dnn_mem_t &src = args.find(DNNL_ARG_SRC);
    const dnn_mem_t &mean = args.find(DNNL_ARG_MEAN);
    const dnn_mem_t &var = args.find(DNNL_ARG_VARIANCE);
    const dnn_mem_t &d_dst = args.find(DNNL_ARG_DIFF_DST);
    const dnn_mem_t &ss
            = args.find(prb->use_sc() ? DNNL_ARG_SCALE : DNNL_ARG_SCALE_SHIFT);
    const dnn_mem_t &d_src = args.find(DNNL_ARG_DIFF_SRC);
    const dnn_mem_t &d_ss = args.find(
            prb->use_sc() ? DNNL_ARG_DIFF_SCALE : DNNL_ARG_DIFF_SCALE_SHIFT);
    const dnn_mem_t &d_sh = args.find(DNNL_ARG_DIFF_SHIFT);

    float *d_src_ptr = (float *)d_src;
    float *d_ss_ptr = (float *)d_ss;
    float *d_sh_ptr = (float *)d_sh;

    const bool use_ss = prb->use_ss();
    const bool use_sc = prb->use_sc();
    const bool use_sh = prb->use_sh();

    if ((use_ss || use_sc || use_sh) && (prb->dir & FLAG_WEI)) {
        benchdnn_parallel_nd(prb->c, [&](int64_t c) {
            float d_gamma = 0;
            float d_beta = 0;

            for (int64_t n = 0; n < prb->n; ++n) {
                float smean = mean.get_elem(n);
                float svar = var.get_elem(n);
                float rcp_denom = 1.f / sqrtf(svar + prb->eps);
                auto off = n * prb->c + c;
                float dd = d_dst.get_elem(off);
                d_gamma += dd * (src.get_elem(off) - smean) * rcp_denom;
                d_beta += dd;
            }

            if (use_ss) {
                d_ss_ptr[c] = d_gamma;
                d_ss_ptr[prb->c + c] = d_beta;
            }

            if (use_sc) d_ss_ptr[c] = d_gamma;
            if (use_sh) d_sh_ptr[c] = d_beta;
        });
    }

    benchdnn_parallel_nd(prb->n, [&](int64_t n) {
        float smean = mean.get_elem(n);
        float svar = var.get_elem(n);
        float rcp_denom = 1.f / sqrtf(svar + prb->eps);
        float dd_gamma = 0, dd_gamma_x = 0;
        if (!(prb->flags & GLOB_STATS)) {
            for (int64_t c = 0; c < prb->c; ++c) {
                auto off = n * prb->c + c;
                float ds = d_dst.get_elem(off);
                const float x = src.get_elem(off) - smean;
                float gamma = use_ss || use_sc ? ss.get_elem(c) : 1;
                dd_gamma += gamma * ds;
                dd_gamma_x += gamma * ds * x;
            }
            dd_gamma_x *= rcp_denom;
        }
        for (int64_t c = 0; c < prb->c; ++c) {
            float gamma = use_ss || use_sc ? ss.get_elem(c) : 1;
            auto off = n * prb->c + c;
            float ds = d_dst.get_elem(off) * gamma;
            if (!(prb->flags & GLOB_STATS)) {
                const float x = src.get_elem(off) - smean;
                ds -= (dd_gamma + x * dd_gamma_x * rcp_denom) / prb->c;
            }

            d_src_ptr[off] = rcp_denom * ds;
        }
    });
}

void compute_ref(
        const prb_t *prb, const args_t &args, dnnl_primitive_t prim_ref) {
    if (prb->dir & FLAG_FWD)
        compute_ref_fwd(prb, args);
    else
        compute_ref_bwd(prb, args);
}

} // namespace lnorm
