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

#include <memory>
#include <stdlib.h>
#include <vector>
#ifndef _WIN32
#include <sys/time.h>
#else
#include <windows.h>
#endif

#include "oneapi/dnnl/dnnl_graph.h"

#include "interface/backend.hpp"
#include "interface/c_types_map.hpp"
#include "interface/partition.hpp"
#include "interface/thread.hpp"

#include "utils/debug.hpp"
#include "utils/utils.hpp"
#include "utils/verbose.hpp"

#ifndef DNNL_GRAPH_VERSION_MAJOR
#define DNNL_GRAPH_VERSION_MAJOR INT_MAX
#endif

#ifndef DNNL_GRAPH_VERSION_MINOR
#define DNNL_GRAPH_VERSION_MINOR INT_MAX
#endif

#ifndef DNNL_GRAPH_VERSION_PATCH
#define DNNL_GRAPH_VERSION_PATCH INT_MAX
#endif

#ifndef DNNL_GRAPH_VERSION_HASH
#define DNNL_GRAPH_VERSION_HASH "N/A"
#endif

#ifndef DNNL_GRAPH_CPU_RUNTIME
#define DNNL_GRAPH_CPU_RUNTIME UINT_MAX
#endif

#ifndef DNNL_GRAPH_GPU_RUNTIME
#define DNNL_GRAPH_GPU_RUNTIME UINT_MAX
#endif

namespace dnnl {
namespace graph {
namespace impl {
namespace utils {

// The following code is derived from oneDNN/src/common/verbose.cpp
double get_msec() {
#ifdef _WIN32
    static LARGE_INTEGER frequency;
    if (frequency.QuadPart == 0) QueryPerformanceFrequency(&frequency);
    LARGE_INTEGER now;
    QueryPerformanceCounter(&now);
    return 1e+3 * now.QuadPart / frequency.QuadPart;
#else
    struct timeval time;
    gettimeofday(&time, nullptr);
    return 1e+3 * static_cast<double>(time.tv_sec)
            + 1e-3 * static_cast<double>(time.tv_usec);
#endif
}

static setting_t<int> verbose {0};
int get_verbose() {
#if !defined(DNNL_GRAPH_DISABLE_VERBOSE)
    if (!verbose.initialized()) {
        // Assumes that all threads see the same environment
        static int val = getenv_int_user("VERBOSE", verbose.get());
        verbose.set(val);
    }
    static bool version_printed = false;
    if (!version_printed && verbose.get() > 0) {
        printf("onednn_graph_verbose,info,oneDNN Graph v%d.%d.%d (commit %s)\n",
                dnnl_graph_version()->major, dnnl_graph_version()->minor,
                dnnl_graph_version()->patch, dnnl_graph_version()->hash);
#if DNNL_GRAPH_CPU_RUNTIME != DNNL_GRAPH_RUNTIME_NONE
        printf("onednn_graph_verbose,info,cpu,runtime:%s,nthr:%d\n",
                dnnl_graph_runtime2str(dnnl_graph_version()->cpu_runtime),
                dnnl_graph_get_max_threads());
#endif
        printf("onednn_graph_verbose,info,gpu,runtime:%s\n",
                dnnl_graph_runtime2str(dnnl_graph_version()->gpu_runtime));
        std::vector<const backend *> &backends
                = backend_registry_t::get_singleton().get_registered_backends();
        for (size_t i = 0; i < backends.size() - 1; ++i) {
            backend *bkd = const_cast<backend *>(backends[i]);
            printf("onednn_graph_verbose,info,backend,%zu:%s\n", i,
                    bkd->get_name().c_str());
        }
        version_printed = true;
    }
#endif
    return verbose.get();
}

#if defined(DNNL_GRAPH_DISABLE_VERBOSE)
void partition_info_t::init(
        const engine_t *engine, const compiled_partition_t *partition) {
    UNUSED(engine);
    UNUSED(partition);
}

#else

namespace {

std::string logical_tensor2dim_str(
        const impl::logical_tensor_t &logical_tenosr) {
    std::string s;

    auto lt = impl::logical_tensor_wrapper_t(logical_tenosr);

    s += ":";
    s += std::to_string(lt.dims()[0]);
    for (int d = 1; d < lt.ndims(); ++d)
        s += ("x" + std::to_string(lt.dims()[d]));

    return s;
}

std::string logical_tensor2layout_str(
        const impl::logical_tensor_t &logical_tensor) {
    std::string s;

    auto lt = impl::logical_tensor_wrapper_t(logical_tensor);

    s += ":";
    if (lt.layout_type() == impl::layout_type::strided) {
        const auto strides = lt.strides();
        for (int i = 0; i < lt.ndims() - 1; ++i) {
            s += std::to_string(strides[i]);
            s += "s";
        }
        s += std::to_string(strides[lt.ndims() - 1]);
    } else if (lt.layout_type() == impl::layout_type::opaque) {
        s += std::to_string(lt.layout_id());
    } else if (lt.layout_type() == impl::layout_type::any) {
        s += "any";
    } else {
        assert(!"layout type must be any, strided or opaque.");
    }

    return s;
}

std::string logical_tensor2str(const impl::logical_tensor_t &logical_tensor) {
    std::string s;

    s += std::string(data_type2str(logical_tensor.data_type));
    s += ":";
    s += std::to_string(logical_tensor.id);
    s += ":";
    s += std::string(layout_type2str(logical_tensor.layout_type));
    s += ":";
    s += std::string(property_type2str(logical_tensor.property));

    return s;
}

std::string partition2fmt_str(const impl::partition_t &partition) {
    std::string s;

    const std::vector<std::shared_ptr<graph::impl::op_t>> &operators
            = partition.get_ops();
    const size_t num_operator = operators.size();
    if (num_operator == 0) return s;

    bool data_filled = false;
    bool filter_filled = false;
    for (size_t i = 0; i < num_operator; ++i) {
        const std::shared_ptr<graph::impl::op_t> op = operators[i];
        if (op->has_attr(op_attr::data_format)) {
            // If the first i ops have no data_format, empty string with suffix
            // `;` should be printed out for each of them.
            if (!data_filled) {
                s += "data:";
                for (size_t ii = 0; ii < i; ++ii)
                    s += ";";
                // Indicates that at least one op in the list have data format
                // spec.
                data_filled = true;
            }
            const auto data_format
                    = op->get_attr<std::string>(op_attr::data_format);
            if (i == num_operator - 1) {
                s += data_format;
                s += " ";
            } else {
                s += data_format;
                s += ";";
            }
        } else if (data_filled) {
            // If at least one op have data format, op without format spec
            // should give `;` except the last one of data which should give
            // ` `.
            if (i == num_operator - 1) {
                s += " ";
            } else {
                s += ";";
            }
        }
    }
    for (size_t i = 0; i < num_operator; ++i) {
        const std::shared_ptr<graph::impl::op_t> op = operators[i];
        if (op->has_attr(op_attr::filter_format)) {
            if (!filter_filled) {
                s += "filter:";
                for (size_t ii = 0; ii < i; ++ii)
                    s += ";";
                filter_filled = true;
            }
            const auto filter_format
                    = op->get_attr<std::string>(op_attr::filter_format);
            if (i == num_operator - 1) {
                s += filter_format;
                s += " ";
            } else {
                s += filter_format;
                s += ";";
            }
        } else if (filter_filled) {
            s += ";";
        }
    }

    return s;
}

std::string init_info_partition(const impl::engine_t *engine,
        const impl::compiled_partition_t *compiled_partition) {
    std::stringstream ss;

    const auto &partition = compiled_partition->src_partition();

    ss << std::string(engine_kind2str(engine->kind())) << "," << partition.id()
       << "," << partition_kind2str(partition.get_kind()) << ",";

    const std::vector<std::shared_ptr<graph::impl::op_t>> &operators
            = partition.get_ops();
    const size_t num_operators = operators.size();
    for (size_t i = 0; i < num_operators; ++i) {
        ss << operators[i]->get_name()
           << ((i == num_operators - 1) ? "," : ";");
    }

    ss << partition2fmt_str(partition) << ",";
    {
        const auto &inputs = compiled_partition->get_inputs();
        const size_t inputs_size = inputs.size();
        for (size_t i = 0; i < inputs_size; ++i) {
            ss << "in" << i << "_" << logical_tensor2str(inputs[i])
               << logical_tensor2dim_str(inputs[i])
               << logical_tensor2layout_str(inputs[i]) << " ";
        }
    }

    {
        const auto &outputs = compiled_partition->get_outputs();
        const size_t outputs_size = outputs.size();
        for (size_t i = 0; i < outputs_size; ++i) {
            ss << "out" << i << "_" << logical_tensor2str(outputs[i])
               << logical_tensor2dim_str(outputs[i])
               << logical_tensor2layout_str(outputs[i]);
            if (i < outputs_size - 1) ss << " ";
        }
    }

    ss << ",fpm:" << fpmath_mode2str(partition.get_pimpl()->get_fpmath_mode());

    ss << "," << partition.get_assigned_backend()->get_name();

    return ss.str();
}

} // namespace

void partition_info_t::init(const engine_t *engine,
        const compiled_partition_t *compiled_partition) {
    if (is_initialized_) return;

    std::call_once(initialization_flag_, [&] {
        str_ = init_info_partition(engine, compiled_partition);
        is_initialized_ = true;
    });
}

#endif

} // namespace utils
} // namespace impl
} // namespace graph
} // namespace dnnl

const dnnl_graph_version_t *dnnl_graph_version(void) {
    static const dnnl_graph_version_t ver
            = {DNNL_GRAPH_VERSION_MAJOR, DNNL_GRAPH_VERSION_MINOR,
                    DNNL_GRAPH_VERSION_PATCH, DNNL_GRAPH_VERSION_HASH,
                    DNNL_GRAPH_CPU_RUNTIME, DNNL_GRAPH_GPU_RUNTIME};
    return &ver;
}
