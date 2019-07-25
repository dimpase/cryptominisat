#!/usr/bin/python3

import sys
import glob
import re

PY3 = sys.version_info.major == 3

output_path = sys.argv[1]

def write_predictors(predictors, out, name):
    nums = []
    for pred in predictors:
        num = re.findall(r"all_predictors_{name}_conf([0-9]+).h".format(
            name=name), pred)
        if len(num) > 0:
            nums.append(int(num[0]))

    if len(nums) == 0:
        print("ERROR: Cannot calculate number of predictors '{name}'"
              .format(name=name))
        print("ERROR: Maybe you didn't generate the predictors?")
        exit(-1)

    out.write("""    should_keep_{name}_funcs.resize({num});\n""".format(
        num =max(nums)+1, name=name))

    # NULL it out all
    for num in range(max(nums)+1):
        out.write("""    should_keep_{name}_funcs[{num}] = vector<keep_func_type>();\n""".format(num=num, name=name))

    # set the correct value
    for num in sorted(nums):
        out.write("""    should_keep_{name}_funcs[{num}] = should_keep_{name}_conf{num}_funcs;\n""".format(num=num, name=name))


with open(output_path, 'w') as out:
    out.write("""/******************************************
Copyright (c) 2018, Mate Soos

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

//automated
""")
    predictors = glob.glob("all_predictors_*.h")
    clusters = glob.glob("clustering_*.h")
    for x in predictors+clusters:
        out.write('#include "predict/%s"\n' % x)

    out.write("""
#include "clustering.h"
#include "predict_func_type.h"
#include <vector>
using std::vector;

namespace CMSat {

vector<vector<keep_func_type>> should_keep_short_funcs;
vector<vector<keep_func_type>> should_keep_long_funcs;

void fill_pred_funcs() {
    //automated\n""")
    write_predictors(predictors, out, "short")
    out.write("""\n""")
    write_predictors(predictors, out, "long")
    out.write("""
}

//////////
//Function exists checks
//////////

bool short_pred_func_exists(size_t conf) {
    return should_keep_short_funcs.size() > conf && !should_keep_short_funcs[conf].empty();
}

bool long_pred_func_exists(size_t conf) {
    return should_keep_long_funcs.size() > conf && !should_keep_long_funcs[conf].empty();
}

//////////
//Function returns
//////////

const vector<keep_func_type>& get_short_pred_keep_funcs(size_t conf) {
    assert(short_pred_func_exists(conf));
    return should_keep_short_funcs[conf];
}

const vector<keep_func_type>& get_long_pred_keep_funcs(size_t conf) {
    assert(long_pred_func_exists(conf));
    return should_keep_long_funcs[conf];
}

}
""")
