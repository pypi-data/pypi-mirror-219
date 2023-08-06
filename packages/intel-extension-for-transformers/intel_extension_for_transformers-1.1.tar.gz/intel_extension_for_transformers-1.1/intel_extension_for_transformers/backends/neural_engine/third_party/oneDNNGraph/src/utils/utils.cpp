/*******************************************************************************
* Copyright 2021-2022 Intel Corporation
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

#ifdef _WIN32
#include <windows.h>
#endif

#include <climits>
#include <cstdlib>
#include <cstring>

#include "utils/utils.hpp"

namespace dnnl {
namespace graph {
namespace impl {
namespace utils {

int getenv(const char *name, char *buffer, int buffer_size) {
    if (name == nullptr || buffer_size < 0
            || (buffer == nullptr && buffer_size > 0))
        return INT_MIN;

    int result = 0;
    int term_zero_idx = 0;
    size_t value_length = 0;

#ifdef _WIN32
    value_length = GetEnvironmentVariable(name, buffer, buffer_size);
#else
    const char *value = ::getenv(name);
    value_length = value == nullptr ? 0 : strlen(value);
#endif

    if (value_length > INT_MAX)
        result = INT_MIN;
    else {
        int int_value_length = (int)value_length;
        if (int_value_length >= buffer_size) {
            result = -int_value_length;
        } else {
            term_zero_idx = int_value_length;
            result = int_value_length;
#ifndef _WIN32
            if (value) strncpy(buffer, value, buffer_size - 1);
#endif
        }
    }

    if (buffer != nullptr) buffer[term_zero_idx] = '\0';
    return result;
}

int getenv_int(const char *name, int default_value) {
    int value = default_value;
    // # of digits in the longest 32-bit signed int + sign + terminating null
    const int len = 12;
    char value_str[len]; // NOLINT
    if (getenv(name, value_str, len) > 0) value = std::atoi(value_str);
    return value;
}

int getenv_int_user(const char *name, int default_value) {
    int value = default_value;
    // # of digits in the longest 32-bit signed int + sign + terminating null
    const int len = 12;
    char value_str[len]; // NOLINT
    for (const auto &prefix : {"ONEDNN_GRAPH_", "DNNL_GRAPH_"}) {
        std::string name_str = std::string(prefix) + std::string(name);
        if (getenv(name_str.c_str(), value_str, len) > 0) {
            value = std::atoi(value_str);
            break;
        }
    }
    return value;
}

int getenv_int_internal(const char *name, int default_value) {
    int value = default_value;
    // # of digits in the longest 32-bit signed int + sign + terminating null
    const int len = 12;
    char value_str[len]; // NOLINT
    for (const auto &prefix : {"_ONEDNN_GRAPH_", "_DNNL_GRAPH_"}) {
        std::string name_str = std::string(prefix) + std::string(name);
        if (getenv(name_str.c_str(), value_str, len) > 0) {
            value = std::atoi(value_str);
            break;
        }
    }
    return value;
}

std::string getenv_string_user(const char *name) {
    // Random number to fit possible string input.
    std::string value;
    const int len = 32;
    char value_str[len]; // NOLINT
    for (const auto &prefix : {"ONEDNN_", "DNNL_"}) {
        std::string name_str = std::string(prefix) + std::string(name);
        if (getenv(name_str.c_str(), value_str, len) > 0) {
            value = value_str;
            break;
        }
    }
    std::transform(value.begin(), value.end(), value.begin(), ::tolower);
    return value;
}

bool check_verbose_string_user(const char *name, const char *expected) {
    // Random number to fit possible string input.
    std::string value;
    const int len = 64;
    char value_str[len]; // NOLINT
    for (const auto &prefix : {"ONEDNN_GRAPH_", "DNNL_GRAPH_"}) {
        std::string name_str = std::string(prefix) + std::string(name);
        if (getenv(name_str.c_str(), value_str, len) > 0) {
            value = value_str;
            break;
        }
    }
    std::transform(value.begin(), value.end(), value.begin(), ::tolower);
    std::vector<std::string> splits;
    std::string split;
    std::istringstream ss(value);
    while (std::getline(ss, split, ',')) {
        splits.push_back(split);
    }
    return std::find(splits.begin(), splits.end(), std::string(expected))
            != splits.end();
}

} // namespace utils
} // namespace impl
} // namespace graph
} // namespace dnnl
