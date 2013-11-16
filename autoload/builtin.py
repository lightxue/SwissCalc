#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  lightxue
# Email:   bkmgtp@gmail.com
# Version: 0.01
# Website: https://github.com/lightxue/SwissCalc

import math
import hashlib
import base64
import re
import urllib2
import time

funcs = {
    # String
    'ord'  : ord,
    'chr'  : chr,
    'len'  : len,
    # Util
    'int'  : int,
    'float'  : float,
    'str'  : str,
}

# Numeric

math_funcs = {var : getattr(math, var)
              for var in dir(math) if callable(getattr(math, var))}
funcs.update(math_funcs)

def lg(x):
    '''
    lg(x)

    Return the logarithm of x base 2.
    '''
    return math.log(x, 2)

def ln(x):
    '''
    ln(x)

    Return the logarithm of x base e.
    '''
    return math.log(x)

# String

def _print(*var):
    '''
    print([var, ...])

    Print variables just like print in Python
    '''
    for v in var:
        print v,
    print

funcs['print'] = _print

def printf(fmt, *var):
    '''
    printf(fmt, [var, ...])

    Print formatted string like printf in C
    '''
    print fmt % var

def md5(s):
    '''
    md5(s)

    Return the md5 digest value of s as string of hexadecimal digits
    '''
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def sha1(s):
    '''
    sha1(s)

    Return the sha1 digest value of s as string of hexadecimal digits
    '''
    sha = hashlib.sha1()
    sha.update(s)
    return sha.hexdigest()

def b64encode(s):
    '''
    b64encode(s)

    Return the base64 encode string of s
    '''
    return base64.b64encode(s)

def b64decode(s):
    '''
    b64decode(s)

    Return the base64 decode string of s
    '''
    return base64.b64decode(s)

def uesc(s, encoding='utf-8'):
    '''
    uesc(s, [encoding])

    Convert s to unicode escape string. The default encoding of s is utf-8.

    Return the unicode escape string
    '''
    return s.decode(encoding).encode('unicode-escape')

def uunesc(s, encoding='utf-8'):
    '''
    uunesc(s, [encoding])

    Decode s from  unicode escape string to string. The default encoding of decode string is utf-8

    Return the decoe string
    '''
    return s.decode('unicode-escape').encode(encoding)

def sesc(s):
    '''
    sesc(s)

    Return the string escape value of s
    '''
    return s.encode('string-escape')

def sunesc(s):
    '''
    sunesc(s)

    Return the value of unescape string s
    '''
    return s.decode('string-escape')

def urlencode(s):
    '''
    urlencode(s)

    Return the url encode string of s
    '''
    return urllib2.quote(s)

def urldecode(s):
    '''
    urldecode(s)

    Return the url decode string of s
    '''
    return urllib2.unquote(s)

def rot13(s):
    '''
    rot13(s):

    Return caesar-cypher encryption of the operand
    '''
    return s.encode('rot13')

def encode(s, fr, to):
    '''
    encode(s, from_enc, to_enc)

    Convert string from encoding from_enc to encoding to_enc
    '''
    return s.decode(fr).encode(to)

# Utils

def hex(x):
    '''
    hex(x)

    Print hexadecimal representation of integer or string
    '''
    if isinstance(x ,(int, long)):
        s = '0x{0:x}'.format(x)
        return s
    elif isinstance(x, str):
        s = x.encode('hex')
    else:
        raise Exception("type: %s argument can't be converted to hex" % (type(x)))
    r = [s[i:i+2] for i in xrange(0, len(s), 2)]
    r = [r[i:i+8] for i in xrange(0, len(r), 8)]
    print 'hex: '
    print('\n'.join(' '.join(line) for line in r))

def rsize(n):
    '''
    rsize(n)

    Convert file size from n bytes to human-readable string

    return the human readable-string
    '''
    for s in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
        if n < 1024.0:
            return '%.3f %s' % (n, s)
        n /= 1024.0
    return '%f YiB' % n

def nsize(s):
    '''
    nsize(s)

    Convert human-readable file size to the number of bytes. Ignore parameter's case.

    Example:
        unhumansize('1.5 GiB')
        unhumansize('1e5 GB')
        unhumansize('1G')

    Return the number of bytes
    '''
    unit = 'BKMGTPEZY'
    pat = r'([0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?)\s*([BKMGTPEZY])(i?B)?'
    res = re.findall(pat, s, re.IGNORECASE)
    if not res:
        raise Exception('file size: %s is invalid' % s)
    n, u = float(res[0][0]), res[0][3].upper()
    return int(n * (1024 ** unit.index(u)))

def now():
    '''
    now()

    Return the current timestamp
    '''
    return time.time()

def strftime(stamp, fmt='%Y-%m-%d %H:%M:%S'):
    '''
    strftime(stamp[, fmt]) -> string

    Convert a time stamp to a string according to a format specification.
    '''
    return time.strftime(fmt, time.localtime(stamp))

def strptime(string, fmt='%Y-%m-%d %H:%M:%S'):
    '''
    strptime(string[, fmt]) -> timestamp

    Parse a string to a time stamp according to a format specification.
    '''
    import datetime
    dt = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    return time.mktime(dt.timetuple())

def rand():
    import random
    return random.randint(0, 2 ** 31)

def color(fg, bg=''):
    return
    import vim
    group = 'hicolor' + fg[1:]
    vim.command(r'syn match %s "%s"' % (group, fg))
    vim.command(r'syn cluster hicolor add=%s' % group)
    vim.command(r'hi %s ctermfg=%s' % (group, fg))
    print fg

builtin_funcs = {var : globals()[var]
              for var in dir() if callable(globals()[var])}
funcs.update(builtin_funcs)