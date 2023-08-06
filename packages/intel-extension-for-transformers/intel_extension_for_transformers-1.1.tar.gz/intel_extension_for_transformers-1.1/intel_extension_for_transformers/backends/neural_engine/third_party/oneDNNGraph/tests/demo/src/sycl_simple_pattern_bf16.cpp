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

/// @example sycl_simple_pattern_bf16.cpp
/// @copybrief sycl_simple_pattern_bf16_cpp
/// Annotated version: @ref sycl_simple_pattern_bf16_cpp

/// @page sycl_simple_pattern_bf16_cpp SYCL CPU/GPU example for conv+relu+conv+relu pattern
///
/// > Example code: @ref sycl_simple_pattern_bf16.cpp

#include <assert.h>

#include <algorithm>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <unordered_map>

#include "oneapi/dnnl/dnnl_graph.hpp"
#include "oneapi/dnnl/dnnl_graph_sycl.hpp"

#include "dnnl.hpp"

#include "common/execution_context.hpp"
#include "common/helpers_any_layout.hpp"
#include "common/utils.hpp"

#define assertm(exp, msg) assert(((void)msg, exp))

using namespace dnnl::graph;
using namespace sycl;
using data_type = logical_tensor::data_type;
using layout_type = logical_tensor::layout_type;

// clang-format off
int main(int argc, char **argv) {
    std::cout << "========Example: Conv->ReLU->Conv->ReLU========\n";

    engine::kind engine_kind = parse_engine_kind(argc, argv);

    static auto isa = dnnl::get_effective_cpu_isa();
    if (engine_kind == engine::kind::cpu && isa < dnnl::cpu_isa::avx512_core) {
        printf("Skip bf16 examples for cpu that do not support "
               "avx512_core.");
        return 0;
    }

    // Step 2: Construct a example graph: `conv->relu->conv->relu`
    graph g(engine_kind);

    /// Create logical tensor
    std::cout << "Create logical tensor--------------------------";
    const std::vector<size_t> logical_id {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    std::vector<int64_t> input_dims {8, 3, 227, 227};
    std::vector<int64_t> weight_dims {96, 3, 11, 11};
    std::vector<int64_t> bias_dims {96};
    std::vector<int64_t> weight1_dims {96, 96, 1, 1};
    std::vector<int64_t> bias1_dims {96};
    std::vector<int64_t> dst_dims {8, 96, 55, 55};

    logical_tensor conv0_src_desc {logical_id[0], data_type::bf16, input_dims, layout_type::strided};
    logical_tensor conv0_weight_desc {logical_id[1], data_type::bf16, weight_dims, layout_type::strided};
    logical_tensor conv0_bias_desc {logical_id[2], data_type::bf16, bias_dims, layout_type::strided};
    logical_tensor conv0_dst_desc {logical_id[3], data_type::bf16, dst_dims, layout_type::strided};
    
    op conv0 {0, op::kind::Convolution, {conv0_src_desc, conv0_weight_desc}, {conv0_dst_desc}, "conv0"};
    conv0.set_attr<std::vector<int64_t>>("strides", {4, 4});
    conv0.set_attr<std::vector<int64_t>>("pads_begin", {0, 0});
    conv0.set_attr<std::vector<int64_t>>("pads_end", {0, 0});
    conv0.set_attr<std::vector<int64_t>>("dilations", {1, 1});
    conv0.set_attr<int64_t>("groups", 1);
    conv0.set_attr<std::string>("data_format", "NCX");
    conv0.set_attr<std::string>("filter_format", "OIX");

    logical_tensor conv0_bias_add_dst_desc {logical_id[9], data_type::bf16, dst_dims, layout_type::strided};

    op conv0_bias_add {1, op::kind::BiasAdd, {conv0_dst_desc, conv0_bias_desc}, {conv0_bias_add_dst_desc}, "conv0_bias_add"};

    logical_tensor relu0_dst_desc {logical_id[4], data_type::bf16, dst_dims, layout_type::strided};
    
    op relu0 {2, op::kind::ReLU, {conv0_bias_add_dst_desc}, {relu0_dst_desc}, "relu0"};

    logical_tensor conv1_weight_desc {logical_id[5], data_type::bf16, weight1_dims, layout_type::strided};
    logical_tensor conv1_bias_desc {logical_id[6], data_type::bf16, bias1_dims, layout_type::strided};
    logical_tensor conv1_dst_desc {logical_id[7], data_type::bf16, dst_dims, layout_type::strided};
    
    op conv1 {3, op::kind::Convolution, {relu0_dst_desc, conv1_weight_desc}, {conv1_dst_desc}, "conv1"};
    conv1.set_attr<std::vector<int64_t>>("strides", {1, 1});
    conv1.set_attr<std::vector<int64_t>>("pads_begin", {0, 0});
    conv1.set_attr<std::vector<int64_t>>("pads_end", {0, 0});
    conv1.set_attr<std::vector<int64_t>>("dilations", {1, 1});
    conv1.set_attr<int64_t>("groups", 1);
    conv1.set_attr<std::string>("data_format", "NCX");
    conv1.set_attr<std::string>("filter_format", "OIX");

    logical_tensor conv1_bias_add_dst_desc {logical_id[10], data_type::bf16, dst_dims, layout_type::strided};

    op conv1_bias_add {4, op::kind::BiasAdd, {conv1_dst_desc, conv1_bias_desc}, {conv1_bias_add_dst_desc}, "conv1_bias_add"};

    logical_tensor relu1_dst_desc {logical_id[8], data_type::bf16, dst_dims, layout_type::strided};
    
    op relu1 {5, op::kind::ReLU, {conv1_bias_add_dst_desc}, {relu1_dst_desc}, "relu1"};
    std::cout << "Success!\n";

    std::unordered_map<size_t, op::kind> op_id_kind_map {{0, op::kind::Convolution},
        {1, op::kind::BiasAdd}, {2, op::kind::ReLU}, {3, op::kind::Convolution},
        {4, op::kind::BiasAdd}, {5, op::kind::ReLU}};

    /// Add OP
    std::cout << "Add OP to graph--------------------------------";
    g.add_op(conv0);
    g.add_op(relu0);
    g.add_op(conv1);
    g.add_op(relu1);
    g.add_op(conv0_bias_add);
    g.add_op(conv1_bias_add);
    std::cout << "Success!\n";

    // Step 3: Filter and get partitions
    /// Graph will be filtered into two partitions: `conv0+relu0` and `conv1+relu1`
    /// Setting `DNNL_GRAPH_DUMP=1` can save internal graphs before/after graph fusion into dot files
    std::cout << "Filter and get partition-----------------------";
    auto partitions = g.get_partitions(partition::policy::fusion);
    std::cout << "Success!\n";

    std::cout << "Number of returned partitions: " << partitions.size() << "\n";
    for (size_t i = 0; i < partitions.size(); ++i) {
        std::cout << "Partition[" << partitions[i].get_id()
                  << "]'s supporting status: "
                  << (partitions[i].is_supported() ? "true" : "false") << "\n";
    }

    /// mark the output logical tensors of partition as ANY layout enabled
    std::unordered_set<size_t> id_to_set_any_layout;
    set_any_layout(partitions, id_to_set_any_layout);

    /// assuming framework can give sycl device ,sycl context and sycl queue at this stage
    sycl::queue q = (engine_kind == engine::kind::gpu)
            ? sycl::queue(gpu_selector {}, sycl::property::queue::in_order {})
            : sycl::queue(cpu_selector {}, sycl::property::queue::in_order {});

    allocator alloc = sycl_interop::make_allocator(dnnl::graph::testing::sycl_malloc_wrapper, dnnl::graph::testing::sycl_free_wrapper);
    engine eng = sycl_interop::make_engine(q.get_device(), q.get_context(), alloc);

    /// construct a new stream
    dnnl::graph::stream strm = sycl_interop::make_stream(eng, q);

    std::vector<compiled_partition> c_partitions(partitions.size());

    // mapping from id to tensors
    // need provide queue for later buffer deallocation
    tensor_map tm {q};

    // mapping from id to queried logical tensor from compiled partition
    // used to record the logical tensors that are previously enabled with ANY layout
    std::unordered_map<size_t, logical_tensor> id_to_queried_logical_tensors;

    for (size_t i = 0; i < partitions.size(); ++i) {
        if (partitions[i].is_supported()) {
            std::cout << "\nPartition[" << partitions[i].get_id() << "] is being processed.\n";
            std::vector<logical_tensor> inputs = partitions[i].get_in_ports();
            std::vector<logical_tensor> outputs = partitions[i].get_out_ports();

            /// replace input logical tensor with the queried one
            replace_with_queried_logical_tensors(inputs, id_to_queried_logical_tensors);

            /// update output logical tensors with ANY layout
            update_tensors_with_any_layout(outputs, id_to_set_any_layout);

            std::cout << "Compiling--------------------------------------";
            /// compile to generate compiled partition
            c_partitions[i] = partitions[i].compile(inputs, outputs, eng);
            std::cout << "Success!\n";

            record_queried_logical_tensors(partitions[i].get_out_ports(), c_partitions[i],
                id_to_queried_logical_tensors);

            std::cout << "Creating tensors and allocating memory buffer--";
            std::vector<tensor> input_ts = tm.construct_and_initialize_tensors(inputs, c_partitions[i], eng, 1);
            std::vector<tensor> output_ts = tm.construct_and_initialize_tensors(outputs, c_partitions[i], eng, 0);
            std::cout << "Success!\n";

            std::cout << "Executing compiled partition-------------------";
            /// execute the compiled partition
            sycl_interop::execute(c_partitions[i], strm, input_ts, output_ts);
            std::cout << "Success!\n";
        } else {
            std::vector<size_t> unsupported_op_ids = partitions[i].get_ops();
            assertm(unsupported_op_ids.size() == 1, "Unsupported partition only "
                "contains single op.");
            if (op_id_kind_map[unsupported_op_ids[0]] == op::kind::Wildcard) {
                std::cout << "\nWarning (actually an error): partition " << partitions[i].get_id() <<
                        " contains only a Wildcard op which cannot be computed.\n";
            } else {
                /// Users need to write implementation code by themselves.
                continue;
            }
        }
    }
    // wait for all compiled partition's execution finished
    strm.wait();

    // Step 6: Check correctness of the output results
    std::cout << "Check correctness------------------------------";
    std::cout << "Skip!\n";

    std::cout << "============Run Example Successfully===========\n";
    return 0;
}
// clang-format on
