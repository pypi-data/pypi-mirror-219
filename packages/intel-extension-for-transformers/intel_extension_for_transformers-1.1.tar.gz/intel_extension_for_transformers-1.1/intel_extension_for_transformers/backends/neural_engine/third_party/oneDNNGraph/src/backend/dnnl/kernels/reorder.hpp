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

#ifndef BACKEND_DNNL_KERNELS_REORDER_HPP
#define BACKEND_DNNL_KERNELS_REORDER_HPP

#include <algorithm>
#include <memory>
#include <vector>

#include "backend/dnnl/dnnl_partition_impl.hpp"
#include "backend/dnnl/op_executable.hpp"
#include "backend/dnnl/passes/memory_planning.hpp"
#include "backend/dnnl/scratchpad.hpp"
#include "backend/dnnl/thread_local_cache.hpp"

#include "backend/dnnl/passes/compile_ops.hpp"
#include "backend/dnnl/passes/insert_ops.hpp"
#include "backend/dnnl/passes/layout_propagation.hpp"
#include "backend/dnnl/passes/lower.hpp"
#include "backend/dnnl/passes/transform.hpp"
#include "backend/dnnl/passes/utils.hpp"

namespace dnnl {
namespace graph {
namespace impl {
namespace dnnl_impl {

template <bool quantized>
struct reorder_t : public kernel_base_t {
private:
    dnnl::engine p_engine_;
    impl::allocator_t *g_alloc_;

    std::shared_ptr<subgraph_t> subgraph_;
    memory_planner_t memory_planner_;

    std::function<std::shared_ptr<execution_args_set_t>()> resource_ctor_;

public:
    ~reorder_t() override {
        thread_local_cache_t<execution_args_set_t> res_cache;
        res_cache.remove_if_exist(reinterpret_cast<size_t>(this));
    }

    impl::status_t compile_impl(const dnnl_partition_impl_t *part,
            const impl::engine_t *g_engine,
            const std::vector<impl::logical_tensor_t> &inputs,
            const std::vector<impl::logical_tensor_t> &outputs,
            const impl::context_t *context) override {
        UNUSED(context);
        p_engine_ = make_dnnl_engine(*g_engine);
        g_alloc_ = g_engine->get_allocator();

        subgraph_ = std::make_shared<subgraph_t>(part->get_ops(), p_engine_,
                part->get_fpmath_mode(), part->get_use_blocked_layout(), true);
        BACKEND_DNNL_CHECK(
                set_given_inputs_outputs(subgraph_, inputs, outputs));

        subgraph_visualizer_t vis(part->id(), [this](const value_t *val) {
            return this->memory_planner_.get_memory_info(val);
        });
        pass_pipeline_t pipeline(vis);

        BACKEND_DNNL_ADD_PASS(pipeline, lower_down);
        BACKEND_DNNL_ADD_PASS(pipeline, binary_canonicalization);

        if (quantized) {
            BACKEND_DNNL_ADD_PASS(pipeline, fuse_to_int8_reorder);
            BACKEND_DNNL_ADD_PASS(pipeline, fold_mul_scales);
            BACKEND_DNNL_ADD_PASS(pipeline, fold_sum_scales);
            BACKEND_DNNL_ADD_PASS(pipeline, fuse_output_scales);
        }
        BACKEND_DNNL_ADD_PASS(pipeline, fuse_post_ops);
        if (quantized) { BACKEND_DNNL_ADD_PASS(pipeline, fuse_zero_points); }
        // insert_to_group_for_reorder: work for weight prepacking case
        BACKEND_DNNL_ADD_PASS(pipeline, insert_to_group_for_reorder);

        pipeline.reset_visualize_arg(true, false);
        BACKEND_DNNL_ADD_PASS(pipeline, layout_propagation);

        // bind the memory for each op
        auto memory_plan = [&](std::shared_ptr<subgraph_t> &sg) {
            return memory_planner_.run(sg);
        };
        pipeline.reset_visualize_arg(true, true);
        BACKEND_DNNL_ADD_PASS(pipeline, memory_plan);
        BACKEND_DNNL_ADD_PASS(pipeline, compile_ops);

        // Run the added passes
        BACKEND_DNNL_CHECK(pipeline.run(subgraph_));

        // fill information for outputs logical tensors
        for (size_t i = 0; i < outputs.size(); i++) {
            auto &out = const_cast<impl::logical_tensor_t &>(outputs[i]);
            out = subgraph_->outs_[i];
        }

        // generate a hash key for exec_args_mgr
        resource_ctor_ = [this]() {
            return this->memory_planner_.get_exec_args_set().clone();
        };

        return impl::status::success;
    }

    void prepare_args_set(const execution_args_set_t *res,
            const std::vector<impl::tensor_t> &inputs,
            const std::vector<impl::tensor_t> &outputs,
            const scratchpad_t &scratchpad) {
        // update the data of partition in/outputs args
        for (const auto &mem_idx : res->get_mems_use_external_inputs()) {
            mem_idx.first.set_data_handle(
                    inputs[mem_idx.second].get_data_handle());
        }
        for (const auto &mem_idx : res->get_mems_use_external_outputs()) {
            mem_idx.first.set_data_handle(
                    outputs[mem_idx.second].get_data_handle());
        }

        grantor_t var_grantor = memory_planner_.internal_temporary_grantor(
                scratchpad.get_buffer());

        for (auto &mem_offkey : res->get_mems_use_internal_temporary()) {
            mem_offkey.first.set_data_handle(
                    var_grantor.get(mem_offkey.second));
        }
    }

    impl::status_t execute_impl(const impl::stream_t *g_stream,
            const std::vector<impl::tensor_t> &inputs,
            const std::vector<impl::tensor_t> &outputs) override {
        dnnl::stream p_stream = make_dnnl_stream(p_engine_, *g_stream);

        // each thread's own local resource
        thread_local_cache_t<execution_args_set_t> res_cache;
        execution_args_set_t *res = res_cache.get_or_add(
                reinterpret_cast<size_t>(this), resource_ctor_);

        temporary_scratchpad_t scratchpad(
                memory_planner_.total_internal_temporary_size(), p_engine_,
                *g_alloc_);
        assertm(scratchpad.size()
                        >= memory_planner_.total_internal_temporary_size(),
                "no enough scratchpad memory");
        prepare_args_set(res, inputs, outputs, scratchpad);

        for (size_t i = 0; i < subgraph_->execs_.size(); i++) {
            subgraph_->execs_[i]->execute(p_stream, res->get_exec_args()[i]);
        }

        return impl::status::success;
    }

#ifdef DNNL_GRAPH_WITH_SYCL
    impl::status_t sycl_execute_impl(const impl::stream_t *g_stream,
            const std::vector<impl::tensor_t> &inputs,
            const std::vector<impl::tensor_t> &outputs,
            const std::vector<::sycl::event> &sycl_deps,
            ::sycl::event *sycl_event) override {
        auto deps = sycl_deps;
        ::sycl::event returned_event;
        dnnl::stream p_stream = make_dnnl_stream(p_engine_, *g_stream);

        // each thread's own local resource
        thread_local_cache_t<execution_args_set_t> res_cache;
        execution_args_set_t *res = res_cache.get_or_add(
                reinterpret_cast<size_t>(this), resource_ctor_);

        temporary_scratchpad_t scratchpad(
                memory_planner_.total_internal_temporary_size(), p_engine_,
                *g_alloc_);
        assertm(scratchpad.size()
                        >= memory_planner_.total_internal_temporary_size(),
                "no enough scratchpad memory");
        prepare_args_set(res, inputs, outputs, scratchpad);

        for (size_t i = 0; i < subgraph_->execs_.size(); i++) {
            returned_event = subgraph_->execs_[i]->execute_sycl(
                    p_stream, res->get_exec_args()[i], deps);
            deps = {returned_event};
        }

        scratchpad.set_deps(returned_event);
        if (sycl_event) *sycl_event = returned_event;

        return impl::status::success;
    }
#endif

    impl::status_t prepare_inplace_pairs_impl() override {
        inplace_pairs_ = memory_planner_.get_subgraph_inplace_pairs();
        return impl::status::success;
    }
};

using float_reorder = reorder_t</* quantized */ false>;
using quantized_reorder = reorder_t</* quantized */ true>;
} // namespace dnnl_impl
} // namespace impl
} // namespace graph
} // namespace dnnl

#endif
