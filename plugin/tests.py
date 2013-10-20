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

if __name__ == "__main__":
    unittest.main()
if __name__ == "__main__":
    unittest.main()
if __name__ == "__main__":
    unittest.main()