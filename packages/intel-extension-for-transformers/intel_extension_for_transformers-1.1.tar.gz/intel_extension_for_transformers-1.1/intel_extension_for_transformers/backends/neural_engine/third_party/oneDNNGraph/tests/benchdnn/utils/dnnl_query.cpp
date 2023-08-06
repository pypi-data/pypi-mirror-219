/*******************************************************************************
* Copyright 2022 Intel Corporation
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

#include "utils/dnnl_query.hpp"

dnnl_prop_kind_t query_prop_kind(const_dnnl_primitive_desc_t pd) {
    dnnl_prop_kind_t prop_kind = dnnl_prop_kind_undef;
    dnnl_primitive_desc_query(pd, dnnl_query_prop_kind, 0, &prop_kind);
    return prop_kind;
}

dnnl_primitive_kind_t query_prim_kind(const_dnnl_primitive_desc_t pd) {
    dnnl_primitive_kind_t prim_kind = dnnl_undefined_primitive;
    dnnl_primitive_desc_query(pd, dnnl_query_primitive_kind, 0, &prim_kind);
    return prim_kind;
}

std::string query_impl_info(const_dnnl_primitive_desc_t pd) {
    const char *str = nullptr;
    dnnl_primitive_desc_query(pd, dnnl_query_impl_info_str, 0, &str);
    std::string s(str);
    return s;
}

const dnnl_memory_desc_t &query_md(
        const_dnnl_primitive_desc_t pd, dnnl_query_t what, int index) {
    return *dnnl_primitive_desc_query_md(pd, what, index);
}

const dnnl_memory_desc_t &query_md(const_dnnl_primitive_desc_t pd, int index) {
    return query_md(pd, dnnl_query_exec_arg_md, index);
}

dnnl_engine_t query_engine(
        const_dnnl_primitive_desc_t pd, dnnl_query_t engine_type) {
    dnnl_engine_t engine;
    dnnl_primitive_desc_query(pd, engine_type, 0, &engine);
    return engine;
}

int64_t query_mem_consumption(const_dnnl_primitive_desc_t pd) {
    int64_t size = 0;
    dnnl_primitive_desc_query(pd, dnnl_query_memory_consumption_s64, 0, &size);
    return size;
}

int query_n_inputs(const_dnnl_primitive_desc_t pd) {
    return dnnl_primitive_desc_query_s32(pd, dnnl_query_num_of_inputs_s32, 0);
}

int query_n_outputs(const_dnnl_primitive_desc_t pd) {
    return dnnl_primitive_desc_query_s32(pd, dnnl_query_num_of_outputs_s32, 0);
}

const_dnnl_post_ops_t query_post_ops(const_dnnl_primitive_attr_t attr) {
    const_dnnl_post_ops_t post_ops {};
    dnnl_primitive_attr_get_post_ops(attr, &post_ops);
    return post_ops;
}

const_dnnl_post_ops_t query_post_ops(const_dnnl_primitive_desc_t pd) {
    const_dnnl_post_ops_t post_ops {};
    dnnl_primitive_attr_get_post_ops(query_attr(pd), &post_ops);
    return post_ops;
}

const_dnnl_primitive_attr_t query_attr(const_dnnl_primitive_desc_t pd) {
    const_dnnl_primitive_attr_t attr {};
    dnnl_primitive_desc_get_attr(pd, &attr);
    return attr;
}

const_dnnl_primitive_desc_t query_pd(dnnl_primitive_t prim) {
    const_dnnl_primitive_desc_t pd {};
    dnnl_primitive_get_primitive_desc(prim, &pd);
    return pd;
}

const_dnnl_op_desc_t query_op_desc(const_dnnl_primitive_desc_t pd) {
    const_dnnl_op_desc_t op_desc {};
    dnnl_primitive_desc_query(pd, dnnl_query_op_d, 0, &op_desc);
    return op_desc;
}

dnnl_engine_kind_t query_engine_kind(const dnnl_engine_t &engine) {
    dnnl_engine_kind_t engine_kind = dnnl_any_engine;
    dnnl_engine_get_kind(engine, &engine_kind);
    return engine_kind;
}
