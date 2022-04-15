#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2009-2020 Authors of CryptoMiniSat, see AUTHORS file
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import optparse
import random
import os

class PlainHelpFormatter(optparse.IndentedHelpFormatter):

    def format_description(self, description):
        if description:
            return description + "\n"
        else:
            return ""


usage = "usage: %prog [options] "
desc = """Generates an LPN problem
"""


def set_up_parser():
    parser = optparse.OptionParser(usage=usage, description=desc,
                                   formatter=PlainHelpFormatter())

    parser.add_option("--verbose", "-v", action="store_true", default=False,
                      dest="verbose", help="Print more output")

    # for fuzz-testing
    parser.add_option("--seed", "-s", dest="seed", default=1,
                      help="Genereate with this seed", type=int)
    parser.add_option("-n", dest="n", default=8, type=int,
                      help="Functiion width")
    parser.add_option("--output", "-o", dest="samples", default=8, type=int,
                      help="Number of samples")
    parser.add_option("--noise", "-k", dest="noise", default=0.1, type=float,
                      help="Ratio of noise")
    parser.add_option("--tolerance", "-i", dest="tolerance", default=1, type=int,
                      help="Threshold")

    return parser



if __name__ == "__main__":
    # parse opts
    parser = set_up_parser()
    (opts, args) = parser.parse_args()

    print("c Seed:      %3d" % opts.seed)
    print("c n:         %3d" % opts.n)
    print("c Samples:   %3d" % opts.samples)
    print("c Noise:       %-3.2f" % opts.noise)
    print("c Tolerance: %3d" % opts.tolerance)
    random.seed(opts.seed)

    # y[i] = set randomly [[output]]
    # x[i] = data that SAT solver can manipulate
    # val[x][y] = x[i]*y[i]


    fun = []
    for i in range(opts.n):
        fun.append(random.randint(0, 1))

    inputs = []
    for i in range(opts.samples):
        inp = []
        for i2 in range(opts.n):
            inp.append(random.randint(0, 1))
        inputs.append(inp)

    real_outputs = []
    for i in range(opts.samples):
        out = 0
        for a,b in zip(fun, inputs[i]):
            out ^= a*b
        real_outputs.append(out)

    num_incorrect_eqs = 0
    correct_eqs = []
    outputs = []
    for i in range(opts.samples):
        out = real_outputs[i]
        if random.random() < opts.noise:
            out = out ^ 1
            num_incorrect_eqs+=1
            correct_eqs.append(False)
        else:
            correct_eqs.append(True)
        outputs.append(out)

    # print
    print("c equations. FUN[i2]*INPUT[i][i2]")
    for i in range(opts.samples):
        toprint = ""
        for i2 in range(opts.n):
            toprint += "c %d" % fun[i2]
            toprint += "*"
            toprint += "%d" % inputs[i][i2]
            if i2 != opts.n-1:
                toprint += " + "
        toprint += " = %d" % outputs[i]
        toprint += "  -- correct: %s" % correct_eqs[i]
        print(toprint)


    # variable table (sequential):
    # n: function we need to figure out
    # inputs -- n+n+n...n exactly opts.samples times. Total: opts.samples*opts.n
    # outputs -- opts.samples
    # helper functions come here

    v = 1
    vars_fun = []
    for _ in range(opts.n):
        vars_fun.append(v)
        v+=1

    #vars_inputs = []
    #for _ in range(opts.samples):
        #tmp = []
        #for _ in range(opts.n):
            #tmp.append(v)
            #v+=1
        #vars_inputs.append(tmp)

    vars_noise = []
    for _ in range(opts.samples):
        vars_noise.append(v)
        v+=1

    ####################
    ####### Generate CNF
    ####################

    # compute outputs
    for i in range(opts.samples):
        vs = []
        for i2 in range(opts.n):
            # v = inputs[i][i2] * fun[i]
            if inputs[i][i2] == 1:
                vs.append(vars_fun[i2])

        out = "x "
        for x in vs:
            out += "%d " % x

        if outputs[i]:
            out+="%d " % vars_noise[i]
        else:
            out+="-%d " % vars_noise[i]

        out +="0"
        print(out)

    # make noise zero
    for i in range(opts.samples):
        print("-%d 0" % vars_noise[i])













