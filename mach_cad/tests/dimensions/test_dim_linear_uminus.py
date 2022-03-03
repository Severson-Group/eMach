import unittest

import model_obj
from model_obj.dimensions import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)
elevenInches = DimInch(11)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)
fiftyMillimeters = DimMillimeter(50)
two54Millimeters = DimMillimeter(254)


class TestUSubtraction(unittest.TestCase):
    def test_single_dimension(self):
        val = -oneInch
        expected = DimInch(-1)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = -twoInches
        expected = DimInch(-2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = -oneMillimeter
        expected = DimMillimeter(-1)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = -two54Millimeters
        expected = DimMillimeter(-254)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))


if __name__ == '__main__':
    unittest.main()
