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

#include <gtest/gtest.h>

#include "oneapi/dnnl/dnnl_graph.h"

#include "dnnl.h"

#include "test_api_common.h"
#include "test_api_common.hpp"

class test_compile_conv
    : public ::testing::TestWithParam<dnnl_graph_test_conv_params> {
private:
    dnnl_graph_status_t create_logic_tensor(const dims_t &dims,
            dnnl_graph_logical_tensor_t *tensor,
            dnnl_graph_data_type_t data_type, dnnl_graph_layout_type_t ltype,
            uint64_t tid) {
        return dnnl_graph_logical_tensor_init_with_dims(tensor, tid, data_type,
                (int32_t)dims.size(), dims.data(), ltype,
                dnnl_graph_tensor_property_undef);
    }

public:
    void TestConv2d() {
        auto p = ::testing::TestWithParam<
                dnnl_graph_test_conv_params>::GetParam();

        static auto isa = dnnl_get_effective_cpu_isa();
        SKIP_IF(p.engine == dnnl_graph_cpu && p.data_type == dnnl_graph_bf16
                        && isa < dnnl_cpu_isa_avx512_core,
                "Skip test for systems that do not support avx512_core.");

        dnnl_graph_graph_t agraph = NULL;
        dnnl_graph_op_t op = NULL;
        dnnl_graph_partition_t partition = NULL;
        dnnl_graph_compiled_partition_t compiled_partition = NULL;

#define TEST_CONV2D_DESTROY \
    do { \
        dnnl_graph_graph_destroy(agraph); \
        agraph = NULL; \
        dnnl_graph_op_destroy(op); \
        op = NULL; \
        dnnl_graph_partition_destroy(partition); \
        partition = NULL; \
        dnnl_graph_compiled_partition_destroy(compiled_partition); \
        compiled_partition = NULL; \
    } while (0);

        dnnl_graph_logical_tensor_t input;
        dnnl_graph_logical_tensor_t weight;
        dnnl_graph_logical_tensor_t output;
        size_t part_num = 0;

        ASSERT_EQ_SAFE(create_logic_tensor(p.tensor_dims.input_dims, &input,
                               p.data_type, p.tensor_layout.input_layout, 1U),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(create_logic_tensor(p.tensor_dims.weight_dims, &weight,
                               p.data_type, p.tensor_layout.weight_layout, 2U),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(create_logic_tensor(p.tensor_dims.output_dims, &output,
                               p.data_type, p.tensor_layout.output_layout, 3U),
                dnnl_graph_success, TEST_CONV2D_DESTROY);

        api_test_dnnl_graph_graph_create(&agraph, p.engine);
        ASSERT_EQ_SAFE(dnnl_graph_op_create(&op, 1, p.op_kind, "test_op"),
                dnnl_graph_success, TEST_CONV2D_DESTROY);

        dnnl_graph_op_add_input(op, &input);
        dnnl_graph_op_add_input(op, &weight);
        dnnl_graph_op_add_output(op, &output);

        const dnnl_graph_logical_tensor_t *inputs[2] = {&input, &weight};
        const dnnl_graph_logical_tensor_t *outputs[1] = {&output};

        ASSERT_EQ_SAFE(
                dnnl_graph_op_set_attr_s64(op, dnnl_graph_op_attr_strides,
                        p.attr_value.strides.data(),
                        static_cast<int64_t>(p.attr_value.strides.size())),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(
                dnnl_graph_op_set_attr_s64(op, dnnl_graph_op_attr_pads_begin,
                        p.attr_value.pads_begin.data(),
                        static_cast<int64_t>(p.attr_value.pads_begin.size())),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(
                dnnl_graph_op_set_attr_s64(op, dnnl_graph_op_attr_pads_end,
                        p.attr_value.pads_end.data(),
                        static_cast<int64_t>(p.attr_value.pads_end.size())),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(
                dnnl_graph_op_set_attr_s64(op, dnnl_graph_op_attr_dilations,
                        p.attr_value.dilations.data(),
                        static_cast<int64_t>(p.attr_value.dilations.size())),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(dnnl_graph_op_set_attr_s64(op, dnnl_graph_op_attr_groups,
                               p.attr_value.groups.data(), 0U),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(dnnl_graph_op_set_attr_str(
                               op, dnnl_graph_op_attr_data_format, "NCX", 1U),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(dnnl_graph_op_set_attr_str(
                               op, dnnl_graph_op_attr_filter_format, "OIX", 1U),
                dnnl_graph_success, TEST_CONV2D_DESTROY);

        ASSERT_EQ_SAFE(dnnl_graph_add_op(agraph, op), dnnl_graph_success,
                TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(dnnl_graph_graph_filter(agraph, p.policy),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(dnnl_graph_graph_get_partition_num(agraph, &part_num),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(part_num, 1U, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(dnnl_graph_partition_create(&partition),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(
                dnnl_graph_graph_get_partitions(agraph, part_num, &partition),
                dnnl_graph_success, TEST_CONV2D_DESTROY);
        ASSERT_EQ_SAFE(dnnl_graph_compiled_partition_create(
                               &compiled_partition, partition),
                dnnl_graph_success, TEST_CONV2D_DESTROY);

        dnnl_graph_engine_t e;
        api_test_dnnl_graph_engine_create(&e, p.engine);
        ASSERT_EQ_SAFE(dnnl_graph_partition_compile(partition,
                               compiled_partition, 2, inputs, 1, outputs, e),
                dnnl_graph_success, TEST_CONV2D_DESTROY);

        // Check in-place pairs
        size_t num_inplace_pairs = 10; // Initialized with an impossible value.
        const dnnl_graph_inplace_pair_t *inplace_pairs = nullptr;
        EXPECT_EQ(
                dnnl_graph_compiled_partition_get_inplace_ports(
                        compiled_partition, &num_inplace_pairs, &inplace_pairs),
                dnnl_graph_success);
        // Convolutional operator W/O sum has no in-place operation.
        EXPECT_EQ(num_inplace_pairs, 0U);

        TEST_CONV2D_DESTROY;
#undef TEST_CONV2D_DESTROY
    }
};

INSTANTIATE_TEST_SUITE_P(Test_CompileConv, test_compile_conv,
        ::testing::Values(
                dnnl_graph_test_conv_params {api_test_engine_kind,
                        dnnl_graph_op_convolution,
                        dnnl_graph_partition_policy_max, dnnl_graph_f32,
                        {"strides", "pads_begin", "pads_end", "dilations",
                                "groups"},
                        {{4, 4}, {0, 0}, {0, 0}, {1, 1}, {1}},
                        {dnnl_graph_layout_type_strided,
                                dnnl_graph_layout_type_strided,
                                dnnl_graph_layout_type_strided},
                        {{1, 3, 227, 227}, {64, 3, 11, 11}, {1, 64, 55, 55}}},
                dnnl_graph_test_conv_params {api_test_engine_kind,
                        dnnl_graph_op_convolution,
                        dnnl_graph_partition_policy_fusion, dnnl_graph_bf16,
                        {"strides", "pads_begin", "pads_end", "dilations",
                                "groups"},
                        {{4, 4}, {0, 0}, {0, 0}, {1, 1}, {1}},
                        {dnnl_graph_layout_type_strided,
                                dnnl_graph_layout_type_strided,
                                dnnl_graph_layout_type_strided},
                        {{1, 3, 227, 227}, {64, 3, 11, 11}, {1, 64, 55, 55}}}));

TEST_P(test_compile_conv, Test_CompileConv) {
    TestConv2d();
}
