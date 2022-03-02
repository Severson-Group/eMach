import unittest

import model_obj
from model_obj.dimensions import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)


class TestAddition(unittest.TestCase):
    def test_single_dimension(self):
        val = oneInch + oneInch
        expected = DimInch(2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneInch + twoInches
        expected = DimInch(3)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter + oneMillimeter
        expected = DimMillimeter(2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter + twoMillimeters
        expected = DimMillimeter(3)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

    def test_different_dimension(self):
        val = oneInch + oneMillimeter
        expected = DimInch(1.0393701)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneInch + oneMillimeter + oneMillimeter
        expected = DimInch(1.0787402)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter + oneInch
        expected = DimMillimeter(26.4)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = twoMillimeters + twoInches
        expected = DimMillimeter(52.8)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))


if __name__ == '__main__':
    unittest.main()
