#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author:  lightxue
# email:   bkmgtp@gmail.com
# version: 0.01
# website: https://github.com/lightxue/SwissCalc

import sys

if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex
from ply.lex import TOKEN
import ply.yacc as yacc
import os
import math

class Parser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        self.funcs = {var : getattr(math, var)
                      for var in dir(math) if callable(getattr(math, var))}
        self.lineno = 0
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] +\
                    "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        self.lexer = lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def execute(self, s):
        if not s:
            return
        yacc.parse(s)

    def run(self):
        while 1:
            try:
                s = raw_input('calc > ')
            except EOFError:
                break
            self.execute(s)

    def _lexme(self, s):
        self.lexer.input(s)
        return [tok for tok in self.lexer]

    def _runlex(self):
        while True:
            try:
                s = raw_input('lexer > ')
            except EOFError:
                break
            for tok in self._lexme(s):
                print tok


class Calc(Parser):
    tokens = (
        'ident',
        'newline',
        'binint', 'octint', 'hexint', 'decint',
        'string',
        'pointfloat', 'exponentfloat',
        'add', 'subtract', 'multiply', 'divide',
        'modulo', 'power', 'factorial',
        'lshift', 'rshift', 'and', 'not', 'or', 'xor',
        'assign',
        'addassign', 'subassign', 'mulassign', 'divassign',
        'modassign', 'powassign',
        'lsftassign', 'rsftassign',
        'andassign', 'orassign', 'xorassign',
        'lparen', 'rparen', 'comma',
    )

    # Tokens

    #t_keyword = r''
    t_ignore = ' \t'
    t_ident = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # numeric operator
    t_add        = r'\+'
    t_subtract   = r'-'
    t_multiply   = r'\*'
    t_divide     = r'/'
    t_modulo     = r'%'
    t_power      = r'\*\*'
    t_factorial  = r'!'

    # bit operator
    t_lshift     = r'<<'
    t_rshift     = r'>>'
    t_and        = r'&'
    t_not        = r'~'
    t_or         = r'\|'
    t_xor        = r'\^'

    # delimiter
    t_assign     = r'='
    t_addassign  = r'\+='
    t_subassign  = r'-='
    t_mulassign  = r'\*='
    t_divassign  = r'/='
    t_modassign  = r'%='
    t_powassign  = r'\*\*='

    t_lsftassign = r'<<='
    t_rsftassign = r'>>='
    t_andassign  = r'&='
    t_orassign   = r'\|='
    t_xorassign  = r'\^='

    t_lparen     = r'\('
    t_rparen     = r'\)'
    t_comma      = r','

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    _escapeseq = r'\\.'
    _stringchar = (r"[^\\']", r'[^\\"]')
    _singlequote = "'(%s|%s)*'" % (_escapeseq, _stringchar[0])
    _doublequote = '"(%s|%s)*"' % (_escapeseq, _stringchar[1])
    _string = r'[rR]?((%s)|(%s))' % (_singlequote, _doublequote)
    @TOKEN(_string)
    def t_string(self, t):
        if t.value[0] in 'rR':
            t.value = t.value[2:-1]
        else:
            t.value = t.value[1:-1].decode('string-escape')
        return t

    def t_exponentfloat(self, t):
        r'[0-9]+(\.[0-9]+)?[eE][+-]?[0-9]+'
        t.value = float(t.value)
        return t

    def t_pointfloat(self, t):
        r'[0-9]+\.[0-9]+'
        t.value = float(t.value)
        return t

    def t_binint(self, t):
        r'0[bB][01]+'
        t.value = int(t.value, 2)
        return t

    def t_octint(self, t):
        r'0[oO]?[0-7]+'
        t.value = int(t.value, 8)
        return t

    def t_hexint(self, t):
        r'0[xX][0-9a-fA-F]+'
        t.value = int(t.value, 16)
        return t

    def t_decint(self, t):
        r'[1-9][0-9]*|0'
        t.value = int(t.value)
        return t

    def t_error(self, t):
        print("Illegal character '%s' in %d line" % (t.value[0], t.lexer.lineno))
        t.lexer.skip(1)

    ## Parsing rules

    precedence = (
        ('left', 'or'),
        ('left', 'xor'),
        ('left', 'and'),
        ('left', 'lshift', 'rshift'),
        ('left', 'add', 'subtract'),
        ('left', 'multiply', 'divide', 'modulo'),
        ('right','usub', 'uadd', 'not'),
        ('left', 'factorial'),
        ('left', 'power'),
        )

    #def p_statement_ident(self, p):
        #'''statement : ident'''
        #print(self.names[p[1]])

    def p_statement_expr(self, p):
        '''statement : expression'''
        if p[1] is None:
            return
        if not self._env['float']:
            p[1] = self.truncint(p[1])
        self.names['_'] = p[1]
        print self.repr_result(p[1])

    def p_statement_newline(self, p):
        '''statement : newline'''
        self.lineno += 1

    def p_statement_assign(self, p):
        '''
        statement : ident assign     expression
                  | ident addassign  expression
                  | ident subassign  expression
                  | ident mulassign  expression
                  | ident divassign  expression
                  | ident modassign  expression
                  | ident powassign  expression
                  | ident lsftassign expression
                  | ident rsftassign expression
                  | ident andassign  expression
                  | ident orassign   expression
                  | ident xorassign  expression
        '''
        if   p[2] == '='   : self.names[p[1]] =   p[3]
        elif p[2] == '+='  : self.names[p[1]] +=  p[3]
        elif p[2] == '-='  : self.names[p[1]] -=  p[3]
        elif p[2] == '*='  : self.names[p[1]] *=  p[3]
        elif p[2] == '/='  : self.names[p[1]] /=  p[3]
        elif p[2] == '%='  : self.names[p[1]] %=  p[3]
        elif p[2] == '**=' : self.names[p[1]] **= p[3]
        elif p[2] == '<<=' : self.names[p[1]] <<= p[3]
        elif p[2] == '>>=' : self.names[p[1]] >>= p[3]
        elif p[2] == '&='  : self.names[p[1]] &=  p[3]
        elif p[2] == '|='  : self.names[p[1]] |=  p[3]
        elif p[2] == '^='  : self.names[p[1]] ^=  p[3]
        if not self._env['float']:
            self.name[p[1]] = self.truncint(self.name[p[1]])

        print self.repr_kv(p[1], self.names[p[1]])

    def p_expression_binop(self, p):
        '''
        expression : expression add expression
                   | expression subtract expression
                   | expression multiply expression
                   | expression divide expression
                   | expression or expression
                   | expression xor expression
                   | expression and expression
                   | expression lshift expression
                   | expression rshift expression
                   | expression modulo expression
                   | expression power expression
        '''
        if   p[2] == '+'  : p[0] = p[1] + p[3]
        elif p[2] == '-'  : p[0] = p[1] - p[3]
        elif p[2] == '*'  : p[0] = p[1] * p[3]
        elif p[2] == '/'  : p[0] = p[1] / p[3]
        elif p[2] == '**' : p[0] = p[1] ** p[3]
        elif p[2] == '|'  : p[0] = p[1] | p[3]
        elif p[2] == '^'  : p[0] = p[1] ^ p[3]
        elif p[2] == '&'  : p[0] = p[1] & p[3]
        elif p[2] == '<<' : p[0] = p[1] << p[3]
        elif p[2] == '>>' : p[0] = p[1] >> p[3]
        elif p[2] == '%'  : p[0] = p[1] % p[3]

    def p_expression_unary(self, p):
        '''expression : subtract expression %prec usub
                      | add expression %prec uadd
                      | not expression
        '''
        if    p[1] == '-' : p[0] = -p[2]
        elif  p[1] == '+' : p[0] =  p[2]
        elif  p[1] == '~' : p[0] = ~p[2]

    def p_expression_factorial(self, p):
        '''expression : expression factorial
        '''
        p[0] = math.factorial(p[1])

    def p_expression_func(self, p):
        'expression : function'
        p[0] = p[1]

    def p_func_with_args(self, p):
        'function : ident lparen arguments rparen'
        if p[1] in self.funcs:
            p[0] = self.funcs[p[1]](*p[3])
        else:
            print('function: %s not found' % p[1])

    def p_func_without_args(self, p):
        'function : ident lparen rparen'
        if p[1] in self.funcs:
            p[0] = self.funcs[p[1]]()
        else:
            print('function: %s not found' % p[1])

    def p_arguments_plural(self, p):
        '''
        arguments : expression comma arguments
        '''
        p[0] = p[3][:]
        p[0].insert(0, p[1])

    def p_arguments_single(self, p):
        '''
        arguments : expression
        '''
        p[0] = [p[1]]

    def p_expression_group(self, p):
        'expression : lparen expression rparen'
        p[0] = p[2]

    def p_expression_str(self, p):
        '''
        expression : string
        '''
        p[0] = p[1]

    def p_expression_number(self, p):
        '''
        expression : integer
                   | float
        '''
        if self._env['float']:
            p[0] = float(p[1])
        else:
            p[0] = int(p[1])

    def p_expression_name(self, p):
        'expression : ident'
        try:
            p[0] = self.names[p[1]]
            if isinstance(p[0], str):
                pass
            elif self._env['float']:
                p[0] = float(p[0])
            else:
                p[0] = int(p[0])
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_integer(self, p):
        '''integer : decint
                   | binint
                   | octint
                   | hexint
        '''
        p[0] = p[1]

    def p_float(self, p):
        '''float : pointfloat
                 | exponentfloat
        '''
        p[0] = p[1]

    def p_error(self, p):
        if p:
            print("Syntax error at '%s' in %d line" % (p.value, self.lineno))
        else:
            print("Syntax error at EOF")

    # Misc
    def __init__(self, **kw):
        super(Calc, self).__init__(**kw)
        self.funcs['vars'] = self.show_names
        self.funcs['env'] = self.env
        self.funcs['setenv'] = self.setenv
        # _ store last result, just like interactive python interpreter
        self.names['_'] = 0
        self.names['pi'] = math.pi
        self.names['e'] = math.e
        self._env = {
            'float'  : 0,
            'signed' : 1,
            'word'   : 8,
            'bin'    : 1,
            'oct'    : 1,
            'dec'    : 1,
            'hex'    : 1,
        }

    def bin_int(self, integer):
        length = 8 * self._env['word']
        s = '{0:0{width}b}'.format(integer, width=length)
        r = [s[i:i+8] for i in xrange(0, len(s), 8)]
        r = [r[i:i+4] for i in xrange(0, len(r), 4)]
        return '\n'.join(' '.join(line) for line in r)

    def oct_int(self, integer):
        return '{0:o}'.format(integer)

    def hex_int(self, integer):
        length = 2 * self._env['word']
        s = '{0:0{width}x}'.format(integer, width=length)
        r = [s[i:i+2] for i in xrange(0, len(s), 2)]
        r = [r[i:i+4] for i in xrange(0, len(r), 4)]
        return '\n'.join(' '.join(line) for line in r)

    def repr_result(self, result):
        if isinstance(result, str) or isinstance(result, float):
            return repr(result)
        res = []
        if self._env['bin']:
            res.append(self.bin_int(result))
        if self._env['oct']:
            res.append(self.oct_int(result))
        if self._env['dec']:
            res.append(repr(result))
        if self._env['hex']:
            res.append(self.hex_int(result))
        return '\n'.join(res)

    def repr_kv(self, key, val):
        return '%s = %s' % (key, repr(val))

    def show_names(self):
        for name, value in self.names.iteritems():
            print self.repr_kv(name, value)

    def env(self):
        names = self._env.keys()
        names.sort(key=len)
        for name in names:
            print self.repr_kv(name.rjust(10), self._env[name])

    def setenv(self, name, value):
        self._env[name] = int(value)

    def truncint(self, val):
        try:
            val = int(val)
            signed = bool(self._env['signed'])
            bits = 1 << (self._env['word'] * 8)
            return (val & (bits - 1)) - bool(val & (bits >> 1)) * signed * bits
        except ValueError:
            return val

if __name__ == '__main__':
    calc = Calc(debug=0)
    calc.run()
