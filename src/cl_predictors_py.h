/******************************************
Copyright (C) 2009-2020 Authors of CryptoMiniSat, see AUTHORS file

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
***********************************************/

#ifndef _CLPREDICTORS_PY_H__
#define _CLPREDICTORS_PY_H__

#include <vector>
#include <cassert>
#include <string>
#include "clause.h"
#include "cl_predictors_abs.h"

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>

#define NUM_RAW_FEATS 42

using std::vector;

namespace CMSat {

class Clause;
class Solver;

class ClPredictorsPy : public ClPredictorsAbst
{
public:
    ClPredictorsPy();
    virtual ~ClPredictorsPy();
    virtual int load_models(
        const std::string& short_fname,
        const std::string& long_fname,
        const std::string& forever_fname,
        const std::string& best_feats_fname) override;
    virtual int load_models_from_buffers() override;

    virtual int set_up_input(
        const CMSat::Clause* const cl,
        const uint64_t sumConflicts,
        const double   act_ranking_rel,
        const double   uip1_ranking_rel,
        const double   prop_ranking_rel,
        const double   sum_uip1_per_time_ranking,
        const double   sum_props_per_time_ranking,
        const double   sum_uip1_per_time_ranking_rel,
        const double   sum_props_per_time_ranking_rel,
        const ReduceCommonData& commdata,
        const Solver* solver,
        float* at) override;

    virtual int get_step_size() override {return NUM_RAW_FEATS;}

    float predict(
        predict_type pred_type,
        const CMSat::Clause* cl,
        const uint64_t sumConflicts,
        const double   act_ranking_rel,
        const double   uip1_ranking_rel,
        const double   prop_ranking_rel,
        const ReduceCommonData& commdata
    );

    virtual void predict_all(
        float* const data,
        uint32_t const num) override;

    virtual void get_prediction_at(ClauseStatsExtra& extdata, const uint32_t at) override;
    virtual void finish_all_predict() override;

private:
    double* out_result[3];
    PyObject *pDict = nullptr;
    PyObject *pFunc = nullptr;
    PyObject *pRet[3];
    PyObject *pArray = nullptr;
    PyObject *pArgs = nullptr;
    PyArrayObject* ret_data[3];
    PyObject* pModule;
};

}

#endif
