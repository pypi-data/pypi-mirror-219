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

#ifndef DNNL_MEMORY_HPP
#define DNNL_MEMORY_HPP

#include "oneapi/dnnl/dnnl.h"

#if DNNL_GPU_RUNTIME == DNNL_RUNTIME_DPCPP
#include "oneapi/dnnl/dnnl_sycl.h"
#endif

#include "common.hpp"
#include "utils/dims.hpp"

#define dnnl_mem_default_value 0xFF

struct dnn_mem_t {
    struct handle_info_t {
        bool is_host_ptr;
        void *ptr;

        bool is_allocate() const { return ptr == DNNL_MEMORY_ALLOCATE; }

        static handle_info_t allocate() {
            return {false, DNNL_MEMORY_ALLOCATE};
        }
    };

    dnn_mem_t() { map(); }
    dnn_mem_t(const dnnl_memory_desc_t &md, dnnl_engine_t engine);
    dnn_mem_t(const dnnl_memory_desc_t &md, dnnl_engine_t engine,
            const handle_info_t &handle_info);

    dnn_mem_t(int ndims, const dnnl_dims_t dims, dnnl_data_type_t dt,
            const std::string &tag, dnnl_engine_t engine);
    dnn_mem_t(const dnnl_memory_desc_t &md, dnnl_data_type_t dt,
            const std::string &tag, dnnl_engine_t engine);
    dnn_mem_t(const dnnl_memory_desc_t &md, dnnl_data_type_t dt,
            dnnl_engine_t engine);

    dnn_mem_t(int ndims, const dnnl_dims_t dims, dnnl_data_type_t dt,
            const dnnl_dims_t strides, dnnl_engine_t engine);

    dnn_mem_t(const dnn_mem_t &rhs, dnnl_data_type_t dt, const std::string &tag,
            dnnl_engine_t engine);

    dnn_mem_t(const dnn_mem_t &rhs) = delete;
    dnn_mem_t &operator=(const dnn_mem_t &rhs) = delete;

    dnn_mem_t &operator=(dnn_mem_t &&rhs) {
        if (&rhs == this) return *this;
        cleanup();

        md_ = rhs.md_;
        m_ = rhs.m_;
        m_padded_ = rhs.m_padded_;
        data_ = rhs.data_;
        is_data_owner_ = rhs.is_data_owner_;
        active_ = rhs.active_;
        engine_kind_ = rhs.engine_kind_;
        engine_ = rhs.engine_;
        is_mapped_ = (bool)rhs.is_mapped_;
        mapped_ptr_ = rhs.mapped_ptr_;

        rhs.active_ = false;
        return *this;
    }
    dnn_mem_t(dnn_mem_t &&rhs) : dnn_mem_t() { *this = std::move(rhs); }

    ~dnn_mem_t() { cleanup(); }

    int reorder(const dnn_mem_t &rhs, const_dnnl_primitive_attr_t attr);
    int reorder(const dnn_mem_t &rhs) { return reorder(rhs, nullptr); }

    size_t size() const;

    int64_t nelems(bool with_padded_dims = false) const {
        auto dims = with_padded_dims ? md_.padded_dims : md_.dims;
        if (ndims() == 0) return 0;

        int64_t n = 1;
        for (int i = 0; i < ndims(); ++i)
            n *= dims[i];
        return n;
    }

    int ndims() const { return md_.ndims; }
    dnnl_data_type_t dt() const { return md_.data_type; }
    size_t sizeof_dt() const;

    void set_dt(dnnl_data_type_t dt) { md_.data_type = dt; }

    template <typename T>
    explicit operator T *() const {
        assert(is_mapped_);
        return static_cast<T *>(mapped_ptr_);
    }

    explicit operator bool() const {
        assert(is_mapped_);
        return bool(mapped_ptr_);
    }

    float get_elem(int64_t idx) const;
    void set_elem(int64_t idx, float value) const;

    int64_t get_scale_idx(
            int64_t data_idx, int scale_mask, const int ndims) const {
        const auto &dims = md_.dims;
        int64_t stride = 1;
        int64_t offset = 0;

        if (scale_mask != 0) {
            for (int i = 0; i < ndims; ++i) {
                int d = ndims - 1 - i;
                auto pos = data_idx % dims[d];
                data_idx /= dims[d];
                if (scale_mask & (1 << d)) {
                    offset += pos * stride;
                    stride *= dims[d];
                }
            }
        }

        return offset;
    }

    int64_t get_scale_idx(int64_t data_idx, int scale_mask) const {
        return get_scale_idx(data_idx, scale_mask, ndims());
    }

    dnnl_engine_t engine() const { return engine_; }
    dnnl_engine_kind_t engine_kind() const { return engine_kind_; }

    bool is_mapped() const { return is_mapped_; }

    bool is_canary_protected() const { return is_canary_protected_; }

    void map() const;
    void unmap() const;

    static dnn_mem_t create_from_host_ptr(
            const dnnl_memory_desc_t &md, dnnl_engine_t engine, void *host_ptr);

    // Increases memory size to catch potential buffer overreads and
    // overwrites. The padded area is filled with a canary value.
    static size_t pad_memory_size(size_t sz, dnnl_engine_kind_t engine_kind,
            bool *was_padded = nullptr);
    // Increases memory descriptor size to catch potential buffer overreads and
    // overwrites. The padded area is filled with a canary value.
    static dnnl_memory_desc_t pad_memory_desc(const dnnl_memory_desc_t &md,
            dnnl_engine_kind_t engine_kind, bool *was_padded = nullptr);
    // Initializes memory descriptor from sporadic tag or strides.
    static dnnl_memory_desc_t init_md(int ndims, const dnnl_dims_t dims,
            dnnl_data_type_t data_type, const std::string &tag,
            const dims_t &strides_ = {});

    /* fields */
    dnnl_memory_desc_t md_ {};
    dnnl_memory_t m_ {};

    // "Base" memory with a canary-padded buffer for buffer overflow
    // protection.
    dnnl_memory_t m_padded_ {};
    bool is_canary_protected_ = false;

private:
    void *data_ = NULL;
    bool is_data_owner_ = false;
    bool active_ = false;

    dnnl_engine_kind_t engine_kind_ = dnnl_any_engine;
    dnnl_engine_t engine_ = NULL;

    mutable bool is_mapped_ = false;
    mutable void *mapped_ptr_ = NULL;

    int initialize_memory_create_sycl(const handle_info_t &handle_info);
    int initialize_memory_create_opencl(const handle_info_t &handle_info);
    int initialize_memory_create(const handle_info_t &handle_info);

    int initialize(const dnnl_memory_desc_t &md, dnnl_data_type_t dt,
            const std::string &tag, dnnl_engine_t engine,
            const handle_info_t &handle_info = handle_info_t::allocate());
    int initialize(const dnnl_memory_desc_t &md, dnnl_engine_t engine,
            const handle_info_t &handle_info = handle_info_t::allocate());
    int initialize(int ndims, const dnnl_dims_t dims, dnnl_data_type_t dt,
            const std::string &tag, dnnl_engine_t engine);
    int initialize(int ndims, const dnnl_dims_t dims, dnnl_data_type_t dt,
            const dnnl_dims_t strides, dnnl_engine_t engine);

    int cleanup();
};

// Checks that zero padding is preserved.
int check_zero_padding(const dnn_mem_t &mem, int arg, res_t *res = nullptr,
        int *error_count = nullptr);

// Checks that the buffer is not overrun if it was protected by a canary.
int check_buffer_overwrite(const dnn_mem_t &mem, int arg, res_t *res = nullptr);

// Returns physical offset by logical one. Logical offset is represented by an
// array pos. If is_pos_padded is true pos represents the position in already
// padded area.
dnnl_dim_t md_off_v(const dnnl_memory_desc_t &md, const dnnl_dims_t pos,
        bool is_pos_padded = false);

#endif
