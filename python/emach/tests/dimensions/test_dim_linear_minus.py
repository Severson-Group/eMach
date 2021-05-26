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


class TestSubtraction(unittest.TestCase):
    def test_single_dimension(self):
        val = oneInch - oneInch
        expected = DimInch(0)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = twoInches - oneInch
        expected = DimInch(1)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = oneMillimeter - oneMillimeter
        expected = DimMillimeter(0)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = twoMillimeters - oneMillimeter
        expected = DimMillimeter(1)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

    def test_different_dimension(self):
        val = elevenInches - two54Millimeters
        expected = DimInch(1)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = elevenInches - two54Millimeters - oneInch
        expected = DimInch(0)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = fiftyMillimeters - oneInch
        expected = DimMillimeter(24.6)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = fiftyMillimeters - twoInches
        expected = DimMillimeter(-0.8)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))


if __name__ == '__main__':
    unittest.main()
