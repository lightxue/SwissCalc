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

class Parser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()


    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
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
        'andassign', 'notassign', 'orassign', 'xorassign',
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
    t_notassign  = r'~='
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
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    ## Parsing rules

    precedence = (
        ('left','add','subtract'),
        ('left','multiply','divide'),
        ('left', 'power'),
        ('right','uminus'),
        )

    def p_statement_ident(self, p):
        '''statement : ident'''
        print(self.names[p[1]])

    def p_statement_expr(self, p):
        '''statement : expression'''
        print(p[1])

    def p_statement_assign(self, p):
        '''statement : ident assign expression'''
        self.names[p[1]] = p[3]

    def p_expression_binop(self, p):
        '''
        expression : expression add expression
                   | expression subtract expression
                   | expression multiply expression
                   | expression divide expression
                   | expression power expression
        '''
        if   p[2] == '+'  : p[0] = p[1] + p[3]
        elif p[2] == '-'  : p[0] = p[1] - p[3]
        elif p[2] == '*'  : p[0] = p[1] * p[3]
        elif p[2] == '/'  : p[0] = p[1] / p[3]
        elif p[2] == '**' : p[0] = p[1] ** p[3]

    def p_expression_uminus(self, p):
        'expression : subtract expression %prec uminus'
        p[0] = -p[2]

    def p_expression_group(self, p):
        'expression : lparen expression rparen'
        p[0] = p[2]

    def p_expression_number(self, p):
        '''
        expression : integer
                   | float
        '''
        p[0] = p[1]

    def p_expression_name(self, p):
        'expression : ident'
        try:
            p[0] = self.names[p[1]]
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
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    calc = Calc(debug=1)
    #calc = Parser()
    #calc._runlex()
    calc.run()
