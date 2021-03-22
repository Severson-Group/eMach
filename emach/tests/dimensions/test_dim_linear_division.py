import unittest

from eMach.python.emach.model_obj import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)


class TestDivision(unittest.TestCase):
    def test_division_scalar(self):
        self.assertAlmostEqual((oneInch / 2), DimInch(0.5), 5, 'Inch Scalar Division Fail')
        self.assertEqual(type(oneInch / 2), type(DimInch(oneInch)), 'Inch Scalar Division Fail')

        self.assertAlmostEqual((oneMillimeter / 2), DimMillimeter(0.5), 5, 'Millimeter Scalar Division Fail')
        self.assertEqual(type(oneMillimeter / 2), type(DimMillimeter(oneMillimeter)), 'Millimeter Scalar Division Fail')

        self.assertAlmostEqual((oneMillimeter / -5), DimMillimeter(-0.2), 5, 'Millimeter Scalar Division Fail')
        self.assertEqual(type(oneMillimeter / 0), type(DimMillimeter(oneMillimeter)), 'Millimeter Scalar Division Fail')

        self.assertAlmostEqual((twoInches / 8), DimInch(0.25), 5, 'Inch Scalar Division Fail')
        self.assertEqual(type(twoInches / 8), type(DimMillimeter(twoInches)), 'Inch Scalar Division Fail')

    def test_division_dimlinear(self):
        self.assertAlmostEqual((oneInch / oneInch), 1, 5, 'Inch Inch Division Fail')
        self.assertEqual(type(oneInch / oneInch), type(float), 'Inch Inch Division Fail')

        self.assertAlmostEqual((twoMillimeters / oneMillimeter), 2, 5, 'Millimeter Millimeter Division Fail')
        self.assertEqual(type(twoMillimeters / oneMillimeter), type(float), 'Millimeter Millimeter Division Fail')

        self.assertAlmostEqual((oneInch / twoMillimeters), 12.7, 5, 'Inch Millimeter Division Fail')
        self.assertEqual(type(oneInch / twoMillimeters), type(float), 'Inch Millimeter Division Fail')


if __name__ == '__main__':
    unittest.main()
