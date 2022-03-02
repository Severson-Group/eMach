import unittest

import model_obj
from model_obj.dimensions import DimInch, DimMillimeter

negOneInch = DimInch(-1)
negTwoInches = DimInch(-2)
neg11Inches = DimInch(-11)

negOneMillimeter = DimMillimeter(-1)
negTwoMillimeters = DimMillimeter(-2)
negFiftyMillimeters = DimMillimeter(-50)
neg254Millimeters = DimMillimeter(-254)


class TestUAddition(unittest.TestCase):
    def test_single_dimension(self):
        val = +negOneInch
        expected = DimInch(1)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = +negTwoInches
        expected = DimInch(2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = +negOneMillimeter
        expected = DimMillimeter(1)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = +neg254Millimeters
        expected = DimMillimeter(254)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))



if __name__ == '__main__':
    unittest.main()
