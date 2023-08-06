/*******************************************************************************
* Copyright 2020-2022 Intel Corporation
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

#ifndef GPU_OCL_GEN9_SOFTMAX_HPP
#define GPU_OCL_GEN9_SOFTMAX_HPP

#include "common/c_types_map.hpp"
#include "common/nstl.hpp"
#include "common/primitive.hpp"
#include "gpu/compute/compute.hpp"
#include "gpu/gpu_primitive.hpp"
#include "gpu/gpu_resource.hpp"
#include "gpu/gpu_softmax_pd.hpp"
#include "gpu/ocl/ocl_stream.hpp"
#include "gpu/ocl/ocl_utils.hpp"
#include "gpu/primitive_conf.hpp"

namespace dnnl {
namespace impl {
namespace gpu {
namespace ocl {

struct gen9_softmax_fwd_t : public gpu_primitive_t {
    using gpu_primitive_t::gpu_primitive_t;
    struct pd_t : public gpu_softmax_fwd_pd_t {
        using gpu_softmax_fwd_pd_t::gpu_softmax_fwd_pd_t;

        DECLARE_COMMON_PD_T("ocl:gen9", gen9_softmax_fwd_t);

        status_t init(engine_t *engine) {
            using namespace dnnl::impl::format_tag;
            auto *compute_engine
                    = utils::downcast<compute::compute_engine_t *>(engine);

            const memory_desc_wrapper src_d(src_md());
            const memory_desc_wrapper dst_d(dst_md());
            const auto src_dt = src_d.data_type();
            const auto dst_dt = dst_d.data_type();

            using namespace data_type;
            using skip_mask_t = primitive_attr_t::skip_mask_t;
            is_nhwc = (src_d.matches_one_of_tag(nwc, nhwc, ndhwc)
                    != format_tag::undef);
            is_blocked = (src_d.matches_one_of_tag(nCw16c, nChw16c, nCdhw16c)
                    != format_tag::undef);

            bool ok = is_fwd() && axis_size() % buffer_size == 0
                    && !memory_desc_ndims_ok(src_md(), dst_md())
                    && axis() == src_d.ndims() - 1
                    && (src_d.is_plain() || is_blocked || is_nhwc)
                    && utils::one_of(src_dt, f32, f16, bf16, u8, s8)
                    && utils::one_of(dst_dt, f32, f16, bf16, u8, s8)
                    && IMPLICATION(utils::one_of(f16, src_dt, dst_dt),
                            compute_engine->mayiuse(
                                    compute::device_ext_t::khr_fp16))
                    && attr()->has_default_values(skip_mask_t::oscale_runtime)
                    && attr_oscale_ok()
                    && set_default_formats() == status::success
                    && compute_engine->mayiuse_sub_group(subgroup_size);
            if (!ok) return status::unimplemented;

            if (is_blocked && src_md()->dims[1] % subgroup_size != 0) {
                return status::unimplemented;
            }

            if (is_nhwc || is_blocked) {
                group_size = subgroup_size * (axis_size() / buffer_size);
            } else {
                group_size = subgroup_size;
            }

            lws[0] = group_size;
            lws[1] = lws[2] = 1;
            gws[0] = utils::array_product(&src_md()->dims[0], ndims() - 1)
                    * group_size;
            gws[1] = gws[2] = 1;

            auto src_padded_dims = src_d.padded_dims();
            mb = src_padded_dims[0] * src_padded_dims[2] * src_padded_dims[3]
                    & src_padded_dims[4];
            return status::success;
        }

        bool is_nhwc = false;
        bool is_blocked = false;
        size_t gws[3] = {};
        size_t lws[3] = {};
        size_t block[3] = {};
        size_t group_size = 0;
        size_t mb = 0;
        const int subgroup_size = 16;
        // 8x16 load and store commands (Vector_Size x Sub_Group_Size)
        const int buffer_size = 128;
    };

    status_t init(engine_t *engine) override {
        if (pd()->has_zero_dim_memory()) return status::success;

        compute::kernel_ctx_t kernel_ctx;

        kernel_ctx.define_int("SOFTMAX_AXIS_IDX", pd()->axis());
        kernel_ctx.define_int("SOFTMAX_AXIS_SIZE", pd()->axis_size());
        kernel_ctx.define_int("SOFTMAX_BUF", pd()->buffer_size);
        kernel_ctx.define_int("GROUP_SIZE", pd()->group_size);
        kernel_ctx.define_int("SUB_GROUP_SIZE", pd()->subgroup_size);
        kernel_ctx.define_int("MB", pd()->mb);
        kernel_ctx.define_int("OC_PADDED", pd()->src_md()->padded_dims[1]);
        kernel_ctx.define_int("OC",
                pd()->is_blocked ? pd()->subgroup_size
                                 : pd()->src_md(0)->padded_dims[1]);
        kernel_ctx.define_int("IS_NHWC", pd()->is_nhwc);
        kernel_ctx.define_int("IS_BLOCKED", pd()->is_blocked);
        kernel_ctx.define_int("IS_FWD", 1);
        kernel_ctx.add_option("-cl-std=CL2.0");
        kernel_ctx.define_int("LOGSOFTMAX", pd()->is_logsoftmax());

        const memory_desc_wrapper dst_mdw(pd()->dst_md());
        const memory_desc_wrapper src_mdw(pd()->src_md());
        const auto dst_md_info = memory_desc_info_t::create(dst_mdw);
        const auto src_md_info = memory_desc_info_t::create(src_mdw);
        def_memory_desc_info(kernel_ctx, dst_md_info, "DST");
        def_memory_desc_info(kernel_ctx, src_md_info, "SRC");
        kernel_ctx.set_data_type(dst_mdw.data_type());
        set_offsets(kernel_ctx, pd()->dst_md(), "DATA");

        for (int i = 0; i < 3; ++i)
            kernel_ctx.define_int(utils::format("BLOCK_%d", i), pd()->block[i]);

        create_kernel(engine, &kernel_, "gen9_softmax_fwd", kernel_ctx);
        if (!kernel_) return status::runtime_error;

        return status::success;
    }

    status_t execute(const exec_ctx_t &ctx) const override {
        return execute_generic(ctx);
    }

    status_t init_res_storage(
            engine_t *engine, gpu_resource_t *r) const override {
        std::unique_ptr<memory_storage_t> tmp_mem_storage;

        memory_desc_t scales_md;
        scales_md.data_type = data_type::f32;
        scales_md.ndims = 1;
        scales_md.dims[0] = 1;
        memory_desc_init_by_tag(scales_md, format_tag::x);
        CHECK(handle_runtime_value(
                engine, SCALES_, &scales_md, tmp_mem_storage));
        r->add_memory_storage(SCALES_, std::move(tmp_mem_storage));
        return status::success;
    }

protected:
    status_t execute_generic(const exec_ctx_t &ctx) const;
    const pd_t *pd() const { return (const pd_t *)primitive_t::pd().get(); }
    compute::kernel_t kernel_;

    status_t handle_runtime_value(engine_t *engine, int arg_idx,
            const memory_desc_t *md,
            std::unique_ptr<memory_storage_t> &mem_storage) const {
        assert(arg_idx == SCALES_);

        const primitive_attr_t &attr = *pd()->attr();
        void *p {nullptr};
        memory_desc_wrapper mdw(*md);
        size_t sz = sizeof(float);
        memory_storage_t *mem_s_ptr;
        status_t status
                = engine->create_memory_storage(&mem_s_ptr, mdw.nelems() * sz);
        if (status != status::success) {
            mem_storage.reset();
            return status;
        }
        mem_storage.reset(mem_s_ptr);
        assert(sizeof(float) == sizeof(int));
        status = mem_storage->map_data(
                &p, nullptr, sizeof(float) * mdw.nelems());
        if (status != status::success) return status;
        if (attr.output_scales_.has_default_values()) {
            utils::array_set((float *)p, (float)1, mdw.nelems());
        } else {
            utils::array_copy((float *)p, attr.output_scales_.scales_,
                    attr.output_scales_.count_);
        }
        status = mem_storage->unmap_data(p, nullptr);
        return status;
    }

    enum { SCALES_ = 0 };
};

struct gen9_softmax_bwd_t : public gpu_primitive_t {
    using gpu_primitive_t::gpu_primitive_t;
    struct pd_t : public gpu_softmax_bwd_pd_t {
        using gpu_softmax_bwd_pd_t::gpu_softmax_bwd_pd_t;

        DECLARE_COMMON_PD_T("ocl:gen9", gen9_softmax_bwd_t);

        status_t init(engine_t *engine) {
            using namespace dnnl::impl::format_tag;

            auto *compute_engine
                    = utils::downcast<compute::compute_engine_t *>(engine);

            const memory_desc_wrapper diff_src_d(diff_src_md());
            const memory_desc_wrapper diff_dst_d(diff_dst_md());
            const memory_desc_wrapper dst_d(dst_md());

            using namespace data_type;
            bool ok = !is_fwd() && axis_size() % buffer_size == 0
                    && !memory_desc_ndims_ok(
                            dst_md(), diff_src_md(), diff_dst_md())
                    && axis() == diff_src_d.ndims() - 1
                    && utils::one_of(diff_src_d.data_type(), f32, bf16)
                    && utils::one_of(diff_dst_d.data_type(), f32, bf16)
                    && compute_engine->mayiuse_sub_group(subgroup_size)
                    && attr()->has_default_values()
                    && set_default_formats() == status::success
                    && diff_dst_d.data_type() == dst_d.data_type();
            if (!ok) return status::unimplemented;

            is_nhwc = (diff_src_d.matches_one_of_tag(nwc, nhwc, ndhwc)
                    != format_tag::undef);
            is_blk = (diff_src_d.matches_one_of_tag(nCw16c, nChw16c, nCdhw16c)
                    != format_tag::undef);
            if (is_nhwc || is_blk) {
                group_size = subgroup_size * (axis_size() / buffer_size);
            } else {
                group_size = subgroup_size;
            }
            lws[0] = group_size;
            lws[1] = lws[2] = 1;
            gws[0] = utils::array_product(
                             &diff_src_md(0)->padded_dims[0], ndims() - 1)
                    * group_size;
            gws[1] = gws[2] = 1;
            batches = diff_src_md(0)->padded_dims[0]
                    * diff_src_md(0)->padded_dims[2];
            return status::success;
        }

        size_t gws[3] = {};
        size_t lws[3] = {};
        size_t block[3] = {};
        size_t group_size = 0;
        size_t batches = 0;
        bool is_nhwc = false;
        bool is_blk = false;
        const int subgroup_size = 16;
        // 8x16 load and store commands (Vector_Size x Sub_Group_Size)
        const int buffer_size = 128;
    };

    status_t init(engine_t *engine) override {
        if (pd()->has_zero_dim_memory()) return status::success;

        compute::kernel_ctx_t kernel_ctx;

        kernel_ctx.define_int("SOFTMAX_AXIS_IDX", pd()->axis());
        kernel_ctx.define_int("SOFTMAX_AXIS_SIZE", pd()->axis_size());
        kernel_ctx.define_int("SOFTMAX_BUF", pd()->buffer_size);
        kernel_ctx.define_int("SUB_GROUP_SIZE", pd()->subgroup_size);
        kernel_ctx.define_int("GROUP_SIZE", pd()->group_size);
        kernel_ctx.define_int("IS_BWD", 1);
        kernel_ctx.define_int("IS_16C", pd()->is_blk);
        kernel_ctx.define_int("BATCH", pd()->batches);
        kernel_ctx.define_int("IC_WO_PADDING", pd()->diff_src_md(0)->dims[1]);
        kernel_ctx.define_int(
                "IC_PADDED", pd()->diff_src_md(0)->padded_dims[1]);
        kernel_ctx.define_int("IC",
                pd()->is_blk ? pd()->subgroup_size
                             : pd()->diff_src_md(0)->padded_dims[1]);
        kernel_ctx.define_int("IS_NHWC", pd()->is_nhwc);
        kernel_ctx.add_option("-cl-std=CL2.0");
        kernel_ctx.define_int("LOGSOFTMAX", pd()->is_logsoftmax());

        const memory_desc_wrapper diff_src_mdw(pd()->diff_src_md());
        const memory_desc_wrapper diff_dst_mdw(pd()->diff_dst_md());
        const auto diff_src_md_info = memory_desc_info_t::create(diff_src_mdw);
        const auto diff_dst_md_info = memory_desc_info_t::create(diff_dst_mdw);
        def_memory_desc_info(kernel_ctx, diff_src_md_info, "SRC");
        def_memory_desc_info(kernel_ctx, diff_dst_md_info, "DST");
        kernel_ctx.set_data_type(pd()->diff_src_md()->data_type);
        set_offsets(kernel_ctx, *pd()->diff_src_md(), "DATA");

        for (int i = 0; i < 3; ++i)
            kernel_ctx.define_int(utils::format("BLOCK_%d", i), pd()->block[i]);

        create_kernel(engine, &kernel_, "gen9_softmax_bwd", kernel_ctx);
        if (!kernel_) return status::runtime_error;

        return status::success;
    }

    status_t execute(const exec_ctx_t &ctx) const override {
        return execute_generic(ctx);
    }

protected:
    status_t execute_generic(const exec_ctx_t &ctx) const;
    const pd_t *pd() const { return (const pd_t *)primitive_t::pd().get(); }
    compute::kernel_t kernel_;
};
} // namespace ocl
} // namespace gpu
} // namespace impl
} // namespace dnnl

#endif
