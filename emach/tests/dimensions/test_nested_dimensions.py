import unittest

from eMach.python.emach.model_obj import DimInch, DimMillimeter


class TestAddition(unittest.TestCase):
    def test_nested_dimensions(self):
        self.assertAlmostEqual((DimMillimeter(DimInch(1))), DimInch(25.4), 5, 'Inch Addition Fail')
        self.assertEqual(type(DimMillimeter(DimInch(1))), type(DimInch(25.4)), 'Inch Addition Fail')

        self.assertAlmostEqual((DimMillimeter(DimMillimeter(DimMillimeter(25.4)))), DimInch(25.4), 5, 'Inch Addition Fail')
        self.assertEqual(type(DimMillimeter(DimMillimeter(DimMillimeter(25.4)))), type(DimInch(25.4)), 'Inch Addition Fail')

        self.assertAlmostEqual((DimInch(DimMillimeter(DimInch(25.4)))), DimInch(25.4), 5, 'Inch Addition Fail')
        self.assertEqual(type(DimInch(DimMillimeter(DimInch(25.4)))), type(DimInch(25.4)), 'Inch Addition Fail')


if __name__ == '__main__':
    unittest.main()
