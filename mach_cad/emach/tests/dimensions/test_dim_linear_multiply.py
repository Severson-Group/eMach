import unittest

import model_obj
from model_obj.dimensions import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)


class TestMultiply(unittest.TestCase):
    def test_multiply_scalar_lhs(self):
        val = 2 * oneInch
        expected = DimInch(2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = 2 * oneMillimeter
        expected = DimMillimeter(2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = 0 * oneMillimeter
        expected = DimMillimeter(0)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = -2 * oneMillimeter
        expected = DimMillimeter(-2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

    def test_multiply_scalar_rhs(self):
        val = oneInch * 2
        expected = DimInch(2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter * 2
        expected = DimMillimeter(2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter * 0
        expected = DimMillimeter(0)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter * -2
        expected = DimMillimeter(-2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

    def test_fail_conditions_multiply(self):
        with self.assertRaises(Exception):
            oneInch * oneInch




if __name__ == '__main__':
    unittest.main()
