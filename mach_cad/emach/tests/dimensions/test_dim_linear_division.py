import unittest

import model_obj
from model_obj.dimensions import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)


class TestDivision(unittest.TestCase):
    def test_division_scalar(self):
        val = oneInch / 2
        expected = DimInch(0.5)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter / 2
        expected = DimMillimeter(0.5)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter / -5
        expected = DimMillimeter(-0.2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = twoInches / 8
        expected = DimInch(0.25)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

    def test_division_dimlinear(self):
        val = oneInch / oneInch
        expected = 1.0
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = twoMillimeters / oneMillimeter
        expected = 2.0
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneInch / twoMillimeters
        expected = 12.7
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

    def test_fail_conditions_divide(self):
        with self.assertRaises(Exception):
            5 / oneInch


if __name__ == '__main__':
    unittest.main()
