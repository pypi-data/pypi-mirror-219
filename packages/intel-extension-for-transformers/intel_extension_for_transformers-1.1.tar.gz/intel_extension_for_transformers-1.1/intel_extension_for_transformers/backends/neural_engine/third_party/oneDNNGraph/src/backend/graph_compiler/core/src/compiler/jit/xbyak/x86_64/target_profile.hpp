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

#ifndef BACKEND_GRAPH_COMPILER_CORE_SRC_COMPILER_JIT_XBYAK_X86_64_TARGET_PROFILE_HPP
#define BACKEND_GRAPH_COMPILER_CORE_SRC_COMPILER_JIT_XBYAK_X86_64_TARGET_PROFILE_HPP

#include <compiler/config/context.hpp>
#include <compiler/jit/xbyak/configured_xbyak.hpp>

#include <map>
#include <vector>

namespace sc {
namespace sc_xbyak {
namespace x86_64 {

enum class call_convention {
    undefined = 0,
    system_v,
    microsoft,
};

struct target_profile_t {
    target_profile_t(const runtime::target_machine_t &target_machine)
        : target_machine_(target_machine) {}

    const runtime::target_machine_t &target_machine_;
    call_convention call_convention_;
    size_t shadow_space_bytes_;
    size_t red_zone_bytes_;

    std::vector<Xbyak::Reg> alloc_gp_regs_;
    std::vector<Xbyak::Reg> alloc_xmm_regs_;
    std::vector<Xbyak::Reg> alloc_mask_regs_;
    std::vector<Xbyak::Reg> alloc_tile_regs_;

    std::vector<Xbyak::Reg> caller_saved_gp_regs_;
    std::vector<Xbyak::Reg> callee_saved_gp_regs_;
    std::vector<Xbyak::Reg> callee_saved_xmm_regs_;

    std::vector<Xbyak::Reg> func_arg_gp_regs_;
    std::vector<Xbyak::Reg> func_arg_xmm_regs_;

    Xbyak::Reg func_return_gp_reg_;
    Xbyak::Reg func_return_xmm_reg_;
};

target_profile_t get_target_profile(
        const runtime::target_machine_t &target_machine);

} // namespace x86_64
} // namespace sc_xbyak
} // namespace sc

#endif
