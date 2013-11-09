import unittest
import swisscalc
import math

class LexTest(unittest.TestCase):
    def test_dec(self):
        calc = swisscalc.Calc()
        tok = calc._lexme('1234')[0]
        self.assertEqual(tok.type, 'decint')
        self.assertEqual(tok.value, 1234)

        tok = calc._lexme('01234')[0]
        self.assertNotEqual(tok.type, 'decint')

        tok = calc._lexme('0')[0]
        self.assertEqual(tok.type, 'decint')
        self.assertEqual(tok.value, 0)

        tok = calc._lexme('123af')[0]
        self.assertEqual(tok.type, 'decint')
        self.assertEqual(tok.value, 123)

    def test_bin(self):
        calc = swisscalc.Calc()
        tok = calc._lexme('0b11')[0]
        self.assertEqual(tok.type, 'binint')
        self.assertEqual(tok.value, 0b11)

        tok = calc._lexme('0B11')[0]
        self.assertEqual(tok.type, 'binint')
        self.assertEqual(tok.value, 0B11)

        tok = calc._lexme('0b132')[0]
        self.assertEqual(tok.type, 'binint')
        self.assertEqual(tok.value, 0b1)

    def test_oct(self):
        calc = swisscalc.Calc()
        tok = calc._lexme('0123')[0]
        self.assertEqual(tok.type, 'octint')
        self.assertEqual(tok.value, 0123)

        tok = calc._lexme('0o123')[0]
        self.assertEqual(tok.type, 'octint')
        self.assertEqual(tok.value, 0o123)

        tok = calc._lexme('0O123')[0]
        self.assertEqual(tok.type, 'octint')
        self.assertEqual(tok.value, 0O123)

        tok = calc._lexme('0789')[0]
        self.assertEqual(tok.type, 'octint')
        self.assertEqual(tok.value, 07)

    def test_hex(self):
        calc = swisscalc.Calc()
        tok = calc._lexme('0x123')[0]
        self.assertEqual(tok.type, 'hexint')
        self.assertEqual(tok.value, 0x123)

        tok = calc._lexme('0X123')[0]
        self.assertEqual(tok.type, 'hexint')
        self.assertEqual(tok.value, 0X123)

        tok = calc._lexme('0xdeadbeefhaha')[0]
        self.assertEqual(tok.type, 'hexint')
        self.assertEqual(tok.value, 0xdeadbeef)

    def test_string(self):
        calc = swisscalc.Calc()

        tok = calc._lexme(r"""'hello'""")[0]
        self.assertEqual(tok.type, 'string')
        self.assertEqual(tok.value, 'hello')

        tok = calc._lexme(r'"world"')[0]
        self.assertEqual(tok.type, 'string')
        self.assertEqual(tok.value, "world")

        tok = calc._lexme(r"""'\'\n'""")[0]
        self.assertEqual(tok.type, 'string')
        self.assertEqual(tok.value, '\'\n')

        tok = calc._lexme(r"""r'\'\n'""")[0]
        self.assertEqual(tok.type, 'string')
        self.assertEqual(tok.value, r'\'\n')

        tok = calc._lexme(r"""R'\'\n'""")[0]
        self.assertEqual(tok.type, 'string')
        self.assertEqual(tok.value, R'\'\n')

        tok = calc._lexme(r'"\"\n"')[0]
        self.assertEqual(tok.type, 'string')
        self.assertEqual(tok.value, "\"\n")

    def test_pointfloat(self):
        calc = swisscalc.Calc()
        tok = calc._lexme('3.14')[0]
        self.assertEqual(tok.type, 'pointfloat')
        self.assertEqual(tok.value, 3.14)

        tok = calc._lexme('0.0001')[0]
        self.assertEqual(tok.type, 'pointfloat')
        self.assertEqual(tok.value, 0.0001)

        tok = calc._lexme('003.14')[0]
        self.assertEqual(tok.type, 'pointfloat')
        self.assertEqual(tok.value, 003.14)

    def test_exponentfloat(self):
        calc = swisscalc.Calc()
        tok = calc._lexme('0e0')[0]
        self.assertEqual(tok.type, 'exponentfloat')
        self.assertEqual(tok.value, 0e0)

        tok = calc._lexme('3.14e-10')[0]
        self.assertEqual(tok.type, 'exponentfloat')
        self.assertEqual(tok.value, 3.14e-10)

        tok = calc._lexme('1.141e+10')[0]
        self.assertEqual(tok.type, 'exponentfloat')
        self.assertEqual(tok.value, 1.141e+10)

        tok = calc._lexme('123e123')[0]
        self.assertEqual(tok.type, 'exponentfloat')
        self.assertEqual(tok.value, 123e123)

    def test_operator(self):
        calc = swisscalc.Calc()

        # numeric operator

        tok = calc._lexme('+')[0]
        self.assertEqual(tok.type, 'add')

        tok = calc._lexme('-')[0]
        self.assertEqual(tok.type, 'subtract')

        tok = calc._lexme('*')[0]
        self.assertEqual(tok.type, 'multiply')

        tok = calc._lexme('/')[0]
        self.assertEqual(tok.type, 'divide')

        tok = calc._lexme('%')[0]
        self.assertEqual(tok.type, 'modulo')

        tok = calc._lexme('**')[0]
        self.assertEqual(tok.type, 'power')

        tok = calc._lexme('!')[0]
        self.assertEqual(tok.type, 'factorial')

        # bit operator

        tok = calc._lexme('<<')[0]
        self.assertEqual(tok.type, 'lshift')

        tok = calc._lexme('>>')[0]
        self.assertEqual(tok.type, 'rshift')

        tok = calc._lexme('&')[0]
        self.assertEqual(tok.type, 'and')

        tok = calc._lexme('~')[0]
        self.assertEqual(tok.type, 'not')

        tok = calc._lexme('|')[0]
        self.assertEqual(tok.type, 'or')

        tok = calc._lexme('^')[0]
        self.assertEqual(tok.type, 'xor')

    def test_delimiter(self):
        calc = swisscalc.Calc()
        tok = calc._lexme('=')[0]
        self.assertEqual(tok.type, 'assign')

        tok = calc._lexme('+=')[0]
        self.assertEqual(tok.type, 'addassign')

        tok = calc._lexme('-=')[0]
        self.assertEqual(tok.type, 'subassign')

        tok = calc._lexme('*=')[0]
        self.assertEqual(tok.type, 'mulassign')

        tok = calc._lexme('/=')[0]
        self.assertEqual(tok.type, 'divassign')

        tok = calc._lexme('%=')[0]
        self.assertEqual(tok.type, 'modassign')

        tok = calc._lexme('**=')[0]
        self.assertEqual(tok.type, 'powassign')

        tok = calc._lexme('<<=')[0]
        self.assertEqual(tok.type, 'lsftassign')

        tok = calc._lexme('>>=')[0]
        self.assertEqual(tok.type, 'rsftassign')

        tok = calc._lexme('&=')[0]
        self.assertEqual(tok.type, 'andassign')

        tok = calc._lexme('|=')[0]
        self.assertEqual(tok.type, 'orassign')

        tok = calc._lexme('^=')[0]
        self.assertEqual(tok.type, 'xorassign')

        tok = calc._lexme('(')[0]
        self.assertEqual(tok.type, 'lparen')

        tok = calc._lexme(')')[0]
        self.assertEqual(tok.type, 'rparen')

        tok = calc._lexme(',')[0]
        self.assertEqual(tok.type, 'comma')

class yacc(unittest.TestCase):
    def test_binop(self):
        calc = swisscalc.Calc()

        ans = calc.execute('3 + 2')
        self.assertEqual(float(ans), 3 + 2)

        ans = calc.execute('3.5 + 1.1')
        self.assertEqual(float(ans), 3.5 + 1.1)

        ans = calc.execute('3 * 2')
        self.assertEqual(float(ans), 3 * 2)

        ans = calc.execute('3.5 * 1.1')
        self.assertEqual(float(ans), 3.5 * 1.1)

        ans = calc.execute('3 / 2')
        self.assertEqual(float(ans), 3 / 2.0)

        ans = calc.execute('3.5 / 1.1')
        self.assertEqual(float(ans), 3.5 / 1.1)

        ans = calc.execute('3 % 2')
        self.assertEqual(float(ans), 3 % 2)

        ans = calc.execute('3.5 % 1.1')
        self.assertEqual(float(ans), 3.5 % 1.1)

        ans = calc.execute('3 ** 2')
        self.assertEqual(float(ans), 3 ** 2)

        ans = calc.execute('3.5 ** 1.1')
        self.assertEqual(float(ans), 3.5 ** 1.1)

        ans = calc.execute('3 << 2')
        self.assertEqual(int(ans), 3 << 2)

        ans = calc.execute('3.5 >> 1.1')
        self.assertEqual(int(ans), 3 >> 1)

        ans = calc.execute('3 >> 2')
        self.assertEqual(int(ans), 3 >> 2)

        ans = calc.execute('3.5 | 1.1')
        self.assertEqual(int(ans), 3 | 1)

        ans = calc.execute('3 & 2')
        self.assertEqual(int(ans), 3 & 2)

        ans = calc.execute('3.5 & 1.1')
        self.assertEqual(int(ans), 3 & 1)

        ans = calc.execute('3 ^ 2')
        self.assertEqual(int(ans), 3 ^ 2)

    def test_unaryop(self):
        calc = swisscalc.Calc()

        ans = calc.execute('8!')
        self.assertEqual(int(ans),  math.factorial(8))

        ans = calc.execute('8.23!')
        self.assertEqual(int(ans), math.factorial(8))

        ans = calc.execute('-8')
        self.assertEqual(int(ans), -8)

        ans = calc.execute('-8.3')
        self.assertEqual(float(ans), -8.3)

        ans = calc.execute('~8')
        self.assertEqual(int(ans), ~8)

    def test_assign(self):
        calc = swisscalc.Calc()

        calc.execute('v = 3')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3)

        calc.execute('v = 3.8')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3.8)

        calc.execute('v = 3')
        calc.execute('v += 3')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3 + 3)

        calc.execute('v = 3.8')
        calc.execute('v += 3.8')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3.8 + 3.8)

        calc.execute('v = 3')
        calc.execute('v -= 3')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3 - 3)

        calc.execute('v = 3.8')
        calc.execute('v -= 3.8')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3.8 - 3.8)

        calc.execute('v = 3')
        calc.execute('v *= 3')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3 * 3)

        calc.execute('v = 3.8')
        calc.execute('v *= 3.8')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3.8 * 3.8)

        calc.execute('v = 3')
        calc.execute('v /= 3')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3 / 3)

        calc.execute('v = 3.8')
        calc.execute('v /= 3.8')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3.8 / 3.8)

        calc.execute('v = 3')
        calc.execute('v %= 3')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3 % 3)

        calc.execute('v = 3.8')
        calc.execute('v %= 3.8')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3.8 % 3.8)

        calc.execute('v = 3')
        calc.execute('v **= 3')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3 ** 3)

        calc.execute('v = 3.8')
        calc.execute('v **= 3.8')
        ans = calc.execute('v')
        self.assertEqual(float(ans), 3.8 ** 3.8)

        calc.execute('v = 3')
        calc.execute('v <<= 3')
        ans = calc.execute('v')
        self.assertEqual(int(ans), 3 << 3)

        calc.execute('v = 3')
        calc.execute('v >>= 3')
        ans = calc.execute('v')
        self.assertEqual(int(ans), 3 >> 3)

        calc.execute('v = 3')
        calc.execute('v &= 3')
        ans = calc.execute('v')
        self.assertEqual(int(ans), 3 & 3)

        calc.execute('v = 3')
        calc.execute('v |= 3')
        ans = calc.execute('v')
        self.assertEqual(int(ans), 3 | 3)

        calc.execute('v = 3')
        calc.execute('v ^= 3')
        ans = calc.execute('v')
        self.assertEqual(int(ans), 3 ^ 3)

    def test_func(self):
        calc = swisscalc.Calc()

        ans = calc.execute('log(2 ** 8, 2)')
        self.assertEqual(float(ans), math.log(2 ** 8, 2))

class InterfaceTest(unittest.TestCase):
    def test_names(self):
        calc = swisscalc.Calc()

        ans = calc.execute('pi')
        self.assertEqual(float(ans), math.pi)

        ans = calc.execute('e')
        self.assertEqual(float(ans), math.e)

if __name__ == "__main__":
    unittest.main()
