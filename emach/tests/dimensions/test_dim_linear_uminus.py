import unittest

from eMach.python.emach.model_obj import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)
elevenInches = DimInch(11)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)
fiftyMillimeters = DimMillimeter(50)
two54Millimeters = DimMillimeter(254)


class TestUSubtraction(unittest.TestCase):
    def test_single_dimension(self):
        self.assertAlmostEqual((-oneInch), DimInch(-1), 5, 'uMinus Inch Fail')
        self.assertEqual(type(-oneInch), type(DimInch(-1)), 'uMinus Inch Fail')

        self.assertAlmostEqual((-twoInches), DimInch(-2), 5, 'uMinus Inch Fail')
        self.assertEqual(type(-twoInches), type(DimInch(-2)), 'uMinus Inch Fail')

        self.assertAlmostEqual((-oneMillimeter), DimMillimeter(-1), 5, 'uMinus Millimeter Fail')
        self.assertEqual(type(-oneMillimeter), type(DimMillimeter(-1)), 'uMinus Millimeter Fail')

        self.assertAlmostEqual((-two54Millimeters), DimMillimeter(-254), 5, 'uMinus Millimeter Fail')
        self.assertEqual(type(-two54Millimeters), type(DimMillimeter(-254)), 'uMinus Millimeter Fail')


if __name__ == '__main__':
    unittest.main()
