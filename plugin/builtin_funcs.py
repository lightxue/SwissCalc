#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author:  lightxue
# email:   bkmgtp@gmail.com
# version: 0.01
# website: https://github.com/lightxue/SwissCalc

import math
import hashlib

funcs = {}

math_funcs = {var : getattr(math, var)
              for var in dir(math) if callable(getattr(math, var))}
funcs.update(math_funcs)

def lg(n):
    return math.log(n, 2)

def ln(n):
    return math.log(n)

def md5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def sha1(s):
    sha = hashlib.sha1()
    sha.update(s)
    return sha.hexdigest()

builtin_funcs = {var : globals()[var]
              for var in dir() if callable(globals()[var])}
funcs.update(builtin_funcs)
