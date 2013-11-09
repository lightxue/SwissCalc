#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  lightxue
# Email:   bkmgtp@gmail.com
# Version: 0.01
# Website: https://github.com/lightxue/SwissCalc

import math
import hashlib

funcs = {
    'ord' : ord,
    'chr' : chr,
}

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

def hex(x):
    if isinstance(x ,int):
        return __builtins__['hex'](x)
    elif isinstance(x, str):
        s = x.encode('hex')
        r = [s[i:i+2] for i in xrange(0, len(s), 2)]
        r = [r[i:i+4] for i in xrange(0, len(r), 4)]
        print '\n'.join(' '.join(line) for line in r)
        return 'hello'
    else:
        raise Exception("hex() argument can't be converted to hex")

def base64(s):
    pass

builtin_funcs = {var : globals()[var]
              for var in dir() if callable(globals()[var])}
funcs.update(builtin_funcs)
