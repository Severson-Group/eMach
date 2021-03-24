import unittest

import model_obj
from model_obj.dimensions import DimInch, DimMillimeter


class TestNestedDimensions(unittest.TestCase):
    def test_nested_dimensions(self):
        val = DimMillimeter(DimInch(1))
        expected = DimMillimeter(25.4)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = DimMillimeter(DimMillimeter(DimMillimeter(25.4)))
        expected = DimMillimeter(25.4)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))

        val = DimInch(DimMillimeter(DimInch(25.4)))
        expected = DimInch(25.4)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))


if __name__ == '__main__':
    unittest.main()
