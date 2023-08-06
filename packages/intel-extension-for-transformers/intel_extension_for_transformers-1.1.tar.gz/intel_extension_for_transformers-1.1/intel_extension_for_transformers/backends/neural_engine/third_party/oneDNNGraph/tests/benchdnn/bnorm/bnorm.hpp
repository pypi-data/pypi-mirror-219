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

#ifndef BNORM_HPP
#define BNORM_HPP

#include <assert.h>
#include <limits.h>
#include <stdint.h>

#include <iostream>
#include <string>

#include "common.hpp"
#include "dnn_types.hpp"
#include "dnnl_common.hpp"
#include "dnnl_debug.hpp"
#include "utils/perf_report.hpp"
#include "utils/settings.hpp"

#ifdef DNNL_EXPERIMENTAL
#include "src/common/experimental.hpp"
#endif

namespace bnorm {

enum check_alg_t { ALG_0, ALG_1, ALG_2, ALG_AUTO };
check_alg_t str2check_alg(const char *str);
const char *check_alg2str(check_alg_t alg);

using flags_t = unsigned;
const flags_t NONE = dnnl_normalization_flags_none;
const flags_t GLOB_STATS = dnnl_use_global_stats;
const flags_t USE_SCALESHIFT = dnnl_use_scaleshift;
const flags_t USE_SCALE = dnnl_use_scale;
const flags_t USE_SHIFT = dnnl_use_shift;
const flags_t FUSE_NORM_RELU = dnnl_fuse_norm_relu;
const flags_t FUSE_NORM_ADD_RELU = dnnl_fuse_norm_add_relu;
flags_t str2flags(const char *str);
std::string flags2str(flags_t flags);

struct desc_t {
    int64_t mb, ic, id, ih, iw;
    float eps;
    std::string name;
    int ndims;

    dims_t data_dims() const;
};
int str2desc(desc_t *desc, const char *str);
std::ostream &operator<<(std::ostream &s, const desc_t &d);

struct settings_t : public base_settings_t {
    settings_t() = default;

    // ctor to save certain fields from resetting
    settings_t(const char *perf_template) : settings_t() {
        this->perf_template = perf_template;
    }

    desc_t desc {};

    std::vector<dir_t> dir {FWD_D};
    std::vector<dnnl_data_type_t> dt {dnnl_f32};
    std::vector<std::string> tag {tag::abx};
    std::vector<flags_t> flags {NONE};
    check_alg_t check_alg = ALG_AUTO;
    bool debug_check_ws = false;

    const char *perf_template_csv() const {
        static const std::string args = "%dir%,%dt%,%tag%,%flags%";
        return perf_template_csv_base(args);
    }

    void reset() { *this = settings_t(perf_template); }
};

struct prb_t : public desc_t {
    prb_t(const desc_t &desc, int64_t mb, dir_t dir, dnnl_data_type_t dt,
            const std::string &tag, flags_t flags, bool inplace,
            const attr_t &attr, check_alg_t check_alg, bool debug_check_ws)
        : desc_t(desc)
        , check_alg(check_alg)
        , debug_check_ws(debug_check_ws)
        , dir(dir)
        , dt(dt)
        , tag(tag)
        , flags(flags)
        , inplace(inplace)
        , attr(attr)
        , user_mb(mb) {
        if (mb) this->mb = mb;
    }
    ~prb_t() {}

    check_alg_t check_alg;
    bool debug_check_ws;

    dir_t dir;
    dnnl_data_type_t dt;
    std::string tag;
    flags_t flags;
    bool inplace;
    attr_t attr;
    int64_t user_mb;

    bool need_ws() const {
        return (flags & (FUSE_NORM_RELU | FUSE_NORM_ADD_RELU))
                && !(dir & FLAG_INF);
    }

    bool use_ss() const { return flags & USE_SCALESHIFT; }
    bool use_sc() const { return flags & USE_SCALE; }
    bool use_sh() const { return flags & USE_SHIFT; }
    bool fuse_relu() const {
        return flags & (FUSE_NORM_RELU | FUSE_NORM_ADD_RELU);
    }
    bool fuse_add_relu() const { return flags & FUSE_NORM_ADD_RELU; }
};
std::ostream &operator<<(std::ostream &s, const prb_t &prb);

struct perf_report_t : public base_perf_report_t {
    perf_report_t(const prb_t *prb, const char *perf_template)
        : base_perf_report_t(perf_template)
        , p_(prb)
        , tag_(normalize_tag(p_->tag, p_->ndims)) {}

    void dump_desc(std::ostream &s) const override {
        s << static_cast<const desc_t &>(*p_);
    }

    void dump_desc_csv(std::ostream &s) const override {
        s << p_->mb << ',' << p_->ic << ',' << p_->id << ',' << p_->ih << ','
          << p_->iw << ',' << p_->eps;
    }

    void dump_flags(std::ostream &s) const override {
        s << flags2str(p_->flags);
    }

    const attr_t *attr() const override { return &p_->attr; }
    const int64_t *user_mb() const override { return &p_->user_mb; }
    const std::string *name() const override { return &p_->name; }
    const dir_t *dir() const override { return &p_->dir; }
    const dnnl_data_type_t *dt() const override { return &p_->dt; }
    const std::string *tag() const override { return &tag_; }

private:
    const prb_t *p_;
    std::string tag_;
};

/* some extra control parameters which shouldn't be placed in prb_t */

inline size_t data_off(const prb_t *prb, int64_t mb, int64_t c, int64_t d,
        int64_t h, int64_t w) {
    return (((mb * prb->ic + c) * prb->id + d) * prb->ih + h) * prb->iw + w;
}

int prepare_fwd(const prb_t *prb, dnn_mem_t &src, dnn_mem_t &src_add,
        dnn_mem_t &mean, dnn_mem_t &var, dnn_mem_t &ss, dnn_mem_t &sh);
int prepare_bwd(const prb_t *prb, dnn_mem_t &mem_dt, dnn_mem_t &mem_fp);
dnnl_status_t init_pd(init_pd_args_t<prb_t> &init_pd_args);

void skip_unimplemented_prb(const prb_t *prb, res_t *res);
void skip_invalid_prb(const prb_t *prb, res_t *res);
void compute_ref(const prb_t *prb, const args_t &args,
        dnnl_primitive_t prim_ref = nullptr);

void setup_cmp(compare::compare_t &cmp, const prb_t *prb, data_kind_t kind,
        const args_t &ref_args);

int doit(const prb_t *prb, res_t *res);
int bench(int argc, char **argv);

} // namespace bnorm

#endif
