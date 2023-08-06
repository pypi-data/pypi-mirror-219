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

#include "backend/dnnl/internal_ops.hpp"
#include "backend/dnnl/kernels/batchnorm.hpp"
#include "backend/dnnl/patterns/fusions.hpp"
#include "backend/dnnl/patterns/transformation_pattern.hpp"
#include "backend/dnnl/patterns/utils.hpp"
namespace dnnl {
namespace graph {
namespace impl {
namespace dnnl_impl {
namespace pattern {

namespace pm = impl::utils::pm;
using in_edges_t = pm::in_edges_t;
using pb_graph_t = pm::pb_graph_t;
using FCreatePattern = impl::pass::FCreatePattern;

/*!
 * \brief This provides batchnorm-related fusion, i.e.
 *        batchnorm-relu fusion
 *        The process includes follow steps:
 *          1. look for fusion pattern on the graph
 *          2. If found, verify if this transformation is safe / correct
 *          3. replace the pattern with a fused op, update the graph
 */

DNNL_BACKEND_REGISTER_PATTERN_DEF_BEGIN(bn_fusion)

DNNL_BACKEND_REGISTER_TRANSFORMATION_PATTERN(dnnl, bn_relu_fusion)
        .set_priority(8.8f)
        .set_kind(impl::partition_kind::batch_norm_post_ops)
        .set_attr<FCreatePattern>("FCreatePattern",
                [](const std::shared_ptr<pb_graph_t> &pgraph) -> void {
                    auto bn = pgraph->append_alternation(
                            std::vector<impl::op_kind_t> {
                                    impl::op_kind::BatchNormInference,
                                    impl::op_kind::BatchNormForwardTraining});
                    bn->append_decision_function(
                            check_input_dtype_from_offset<impl::data_type::f32,
                                    1>);
                    pgraph->append_op(impl::op_kind::ReLU, {in_edge(0, bn, 0)});
                })
        .set_attr<FCreateKernel>("FCreateKernel", []() -> kernel_ptr {
            return std::make_shared<batchnorm_fwd_t>();
        });

#define BATCHNORM_OUTPUT_NUM_CHECK(n1, n2) \
    append_decision_function([](op_t *graph_op) -> bool { \
        return check_output_num<n1>(graph_op) \
                || check_output_num<n2>(graph_op); \
    })

DNNL_BACKEND_REGISTER_TRANSFORMATION_PATTERN(dnnl, bn_bwd_relu_bwd_fusion)
        .set_priority(8.8f)
        .set_kind(impl::partition_kind::misc_post_ops)
        .set_attr<FCreatePattern>("FCreatePattern",
                [](const std::shared_ptr<pb_graph_t> &pgraph) -> void {
                    auto relu_bwd
                            = pgraph->append_op(impl::op_kind::ReLUBackprop);
                    auto bn_bwd = pgraph->append_op(
                            impl::op_kind::BatchNormTrainingBackprop,
                            {in_edge(0, relu_bwd, 0)});
                    bn_bwd->append_decision_function(
                            check_input_dtype_from_offset<impl::data_type::f32,
                                    2>);
                    bn_bwd->BATCHNORM_OUTPUT_NUM_CHECK(1, 3);
                })
        .set_attr<FCreateKernel>("FCreateKernel", []() -> kernel_ptr {
            return std::make_shared<batchnorm_bwd_t>();
        });

DNNL_BACKEND_REGISTER_PATTERN_DEF_END

} // namespace pattern
} // namespace dnnl_impl
} // namespace impl
} // namespace graph
} // namespace dnnl
