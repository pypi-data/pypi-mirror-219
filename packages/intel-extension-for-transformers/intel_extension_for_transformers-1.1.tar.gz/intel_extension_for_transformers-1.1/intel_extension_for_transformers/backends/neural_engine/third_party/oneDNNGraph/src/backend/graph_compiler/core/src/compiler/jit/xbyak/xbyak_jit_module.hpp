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

#ifndef BACKEND_GRAPH_COMPILER_CORE_SRC_COMPILER_JIT_XBYAK_XBYAK_JIT_MODULE_HPP
#define BACKEND_GRAPH_COMPILER_CORE_SRC_COMPILER_JIT_XBYAK_XBYAK_JIT_MODULE_HPP

#include <compiler/jit/jit.hpp>
#include <compiler/jit/xbyak/configured_xbyak.hpp>
#include <compiler/jit/xbyak/sc_xbyak_jit_generator.hpp>
#include <compiler/jit/xbyak/x86_64/native_types.hpp>

#include <memory>
#include <string>

namespace sc {
namespace sc_xbyak {

/**
 * @class xbyak_jit_module
 *
 * Explanation of the inheritence hierarchy:
 *
 * - The two public base classes are required to fit into the Graphcompiler JIT
 *   design.
 *
 * - We want SOME class to inherit from both jit_generator and ir_viewer_t,
 *   as a matter of coding convenience: we can directly call Xbyak-related
 *   codegen functions from the ir_handler callback methods.
 *
 * - We want THIS class to inherit from jit_generator because it's a simple
 *   way to ensure that the memory allocated for the JIT'ed code has the
 *   same lifespan as this xbyak_jit_module.
 */
class xbyak_jit_module : public jit_module,
                         public std::enable_shared_from_this<xbyak_jit_module> {
public:
    virtual ~xbyak_jit_module() = default;

private:
    // NOTE: It may be okay to actually provide these. I just haven't given it
    // much consideration yet. -cconvey
    xbyak_jit_module(xbyak_jit_module &&other) = delete;
    xbyak_jit_module(const xbyak_jit_module &other) = delete;

    // xbyak_jit_engine is this object's factory class.
    friend class xbyak_jit_engine;

    /**
     * @param jit_output - Describes the xbyak jit result.
     * @param globals - Describes the static table base jit_module needs.
     * @param managed_thread_pool - Whether to use managed thread pool
     */
    xbyak_jit_module(std::shared_ptr<sc_xbyak_jit_generator> jit_output,
            statics_table_t &&globals, bool managed_thread_pool);

    std::shared_ptr<sc_xbyak_jit_generator> jit_output_;

public:
    void *get_address_of_symbol(const std::string &name) override;

    std::shared_ptr<jit_function_t> get_function(
            const std::string &name) override;
};

} // namespace sc_xbyak
} // namespace sc

#endif
