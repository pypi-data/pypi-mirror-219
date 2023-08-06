# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/7/2023 5:38 pm
# @Author  : Runsheng
# @File    : primertm.py.py

"""
add post_hoc functions for primerdiffer output, with lines of col4
primername\tprimer_f\tprimer_r\tproduct_len\n
"""

def read_primerdiffer_out(filename):
    lines=[]
    with open(filename, "r") as f:
        for line in f.readlines():
            line_l=line.strip().split("\t")
            lines.append(line_l)
    return lines
