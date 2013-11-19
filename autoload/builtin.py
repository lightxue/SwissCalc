#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author:  lightxue
# Email:   bkmgtp@gmail.com
# Version: 0.01
# Website: https://github.com/lightxue/SwissCalc

import math
import hashlib
import re

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
    printf(fmt[, var, ...])

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

def sha224(s):
    '''
    sha224(s)

    Return the sha224 digest value of s as string of hexadecimal digits
    '''
    sha = hashlib.sha224()
    sha.update(s)
    return sha.hexdigest()

def sha256(s):
    '''
    sha256(s)

    Return the sha256 digest value of s as string of hexadecimal digits
    '''
    sha = hashlib.sha256()
    sha.update(s)
    return sha.hexdigest()

def sha384(s):
    '''
    sha384(s)

    Return the sha384 digest value of s as string of hexadecimal digits
    '''
    sha = hashlib.sha384()
    sha.update(s)
    return sha.hexdigest()

def sha512(s):
    '''
    sha512(s)

    Return the sha512 digest value of s as string of hexadecimal digits
    '''
    sha = hashlib.sha512()
    sha.update(s)
    return sha.hexdigest()

def b64enc(s):
    '''
    b64enc(s)

    Return the base64 encode string of s
    '''
    import base64
    return base64.b64encode(s)

def b64dec(s):
    '''
    b64dec(s)

    Return the base64 decode string of s
    '''
    import base64
    return base64.b64decode(s)

def uesc(s, encoding='utf-8'):
    '''
    uesc(s, [encoding='utf-8'])

    Convert s to unicode escape string. The default encoding of s is utf-8.

    Return the unicode escape string
    '''
    return s.decode(encoding).encode('unicode-escape')

def uunesc(s, encoding='utf-8'):
    '''
    uunesc(s[, encoding='utf-8'])

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

def urlenc(s):
    '''
    urlenc(s)

    Return the url encode string of s
    '''
    import urllib2
    return urllib2.quote(s)

def urldec(s):
    '''
    urldec(s)

    Return the url decode string of s
    '''
    import urllib2
    return urllib2.unquote(s)

def htmlenc(s, quote=0):
    '''
    htmlenc(s[, quote=0])

    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is 1, the quotation mark character (")
    is also translated.")
    '''
    import cgi
    return cgi.escape(s, quote)

def htmldec(s, encoding='utf-8'):
    '''
    htmldec(s[, encoding='utf-8'])

    Return unescape of html entity
    '''
    import HTMLParser
    h = HTMLParser.HTMLParser()
    return h.unescape(s).encode(encoding)

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

def regex(pattern, string):
    '''
    regex(pattern, string)

    Try to apply the regular expression pattern at string and
    print all the match substring or nothing if not match
    '''
    print '\n'.join(re.findall(pattern, string))

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

def ssize(n):
    '''
    ssize(n)

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
    import time
    return time.time()

def strftime(stamp, fmt='%Y-%m-%d %H:%M:%S'):
    '''
    strftime(stamp[, fmt='%Y-%m-%d %H:%M:%S']) -> string

    Convert a time stamp to a string according to a format specification.
    '''
    import time
    return time.strftime(fmt, time.localtime(stamp))

def strptime(string, fmt='%Y-%m-%d %H:%M:%S'):
    '''
    strptime(string[, fmt='%Y-%m-%d %H:%M:%S']) -> timestamp

    Parse a string to a time stamp according to a format specification.
    '''
    import time
    import datetime
    dt = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    return time.mktime(dt.timetuple())

def rand():
    import random
    return random.randint(0, 2 ** 31)

def pjson(s):
    '''
    pjson(s)

    Pretty pring json string
    '''
    import json
    try:
        j = json.loads(s)
    except Exception as err:
        raise Exception('json parse error: %s' % err)
    print json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))

def color(fg, bg=''):
    '''
    color(fg[, bg=''])

    Show color in Vim. Only work for GVim.
    Color string should be RGB format like '#00ff00'
    '''
    import vim
    try:
        fg = re.findall('[0-9a-fA-F]{6}', fg)[0]
        if bg:
            bg = re.findall('[0-9a-fA-F]{6}', bg)[0]
    except:
        raise Exception('color format invalid')

    output = '|' + fg + '-%s' % bg * bool(bg) + '|'
    group = 'hicolor' + output.replace('|', '').replace('-', '')

    vim.command(r'syn match %s "%s"' % (group, output))
    vim.command(r'syn cluster hicolor add=%s' % group)
    vim.command(r'hi %s guifg=#%s' % (group, fg) +
                ' guibg=#%s' % bg * bool(bg))

    print output

builtin_funcs = {var : globals()[var]
              for var in dir() if callable(globals()[var])}
funcs.update(builtin_funcs)
