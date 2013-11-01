#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  lightxue
# Email:   bkmgtp@gmail.com
# Version: 0.01
# Website: https://github.com/lightxue/SwissCalc

# You can define your own functions here
# Every function defined here can be called in SwissCalc
# Your function will overwrite the built-in function if your
#     function's name is the same with built-in function

def example():
    return 'this is an example'

def qbver(n):
    res = []
    for i in xrange(4):
        res.insert(0, str(n & 0xffff))
        n >>= 16
    return '.'.join(res)
