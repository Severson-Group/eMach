import unittest

from eMach.python.emach.model_obj import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)
elevenInches = DimInch(11)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)
fiftyMillimeters = DimMillimeter(50)
two54Millimeters = DimMillimeter(254)


class TestAddition(unittest.TestCase):
    def test_single_dimension(self):
        self.assertAlmostEqual((-oneInch), DimInch(-1), 5, 'Inch Addition Fail')
        self.assertEqual(type(-oneInch), type(DimInch(-1)), 'Inch Addition Fail')

        self.assertAlmostEqual((-twoInches), DimInch(-2), 5, 'Inch Addition Fail')
        self.assertEqual(type(-twoInches), type(DimInch(-2)), 'Inch Addition Fail')

        self.assertAlmostEqual((-oneMillimeter), DimMillimeter(-1), 5, 'Inch Addition Fail')
        self.assertEqual(type(-oneMillimeter), type(DimMillimeter(-1)), 'Inch Addition Fail')

        self.assertAlmostEqual((-two54Millimeters), DimMillimeter(-254), 5, 'Inch Addition Fail')
        self.assertEqual(type(-two54Millimeters), type(DimMillimeter(-254)), 'Inch Addition Fail')


if __name__ == '__main__':
    unittest.main()
