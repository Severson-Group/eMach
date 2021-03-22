import unittest

from eMach.python.emach.model_obj import DimInch, DimMillimeter

negOneInch = DimInch(-1)
negTwoInches = DimInch(-2)
neg11Inches = DimInch(-11)

negOneMillimeter = DimMillimeter(-1)
negTwoMillimeters = DimMillimeter(-2)
negFiftyMillimeters = DimMillimeter(-50)
neg254Millimeters = DimMillimeter(-254)


class TestAddition(unittest.TestCase):
    def test_single_dimension(self):
        self.assertAlmostEqual((+negOneInch), DimInch(1), 5, 'Inch Addition Fail')
        self.assertEqual(type(+negOneInch), type(DimInch(1)), 'Inch Addition Fail')

        self.assertAlmostEqual((+negTwoInches), DimInch(2), 5, 'Inch Addition Fail')
        self.assertEqual(type(+negTwoInches), type(DimInch(2)), 'Inch Addition Fail')

        self.assertAlmostEqual((+negOneMillimeter), DimMillimeter(1), 5, 'Inch Addition Fail')
        self.assertEqual(type(+negOneMillimeter), type(DimMillimeter(1)), 'Inch Addition Fail')

        self.assertAlmostEqual((+neg254Millimeters), DimMillimeter(254), 5, 'Inch Addition Fail')
        self.assertEqual(type(+neg254Millimeters), type(DimMillimeter(254)), 'Inch Addition Fail')


if __name__ == '__main__':
    unittest.main()
