import unittest

from eMach.python.emach.model_obj import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)


class TestMultiply(unittest.TestCase):
    def test_multiply_scalar_lhs(self):
        self.assertAlmostEqual((2 * oneInch), DimInch(2), 5, 'Scalar Inch Multiplication Fail')
        self.assertEqual(type(2 * oneInch), type(DimInch(2)), 'Scalar Inch Multiplication Fail')

        self.assertAlmostEqual((2 * oneMillimeter), DimMillimeter(2), 5, 'Scalar Millimeter Multiplication Fail')
        self.assertEqual(type(2 * oneMillimeter), type(DimMillimeter(2)), 'Scalar Millimeter Multiplication Fail')

        self.assertAlmostEqual((0 * oneMillimeter), DimMillimeter(0), 5, 'Scalar Millimeter Multiplication Fail')
        self.assertEqual(type(0 * oneMillimeter), type(DimMillimeter(0)), 'Scalar Millimeter Multiplication Fail')

        self.assertAlmostEqual((-2 * oneMillimeter), DimMillimeter(-2), 5, 'Scalar Millimeter Multiplication Fail')
        self.assertEqual(type(-2 * oneMillimeter), type(DimMillimeter(-2)), 'Scalar Millimeter Multiplication Fail')

    def test_multiply_scalar_rhs(self):
        self.assertAlmostEqual((oneInch * 2), DimInch(2), 5, 'Inch Scalar Multiplication Fail')
        self.assertEqual(type(oneInch * 2), type(DimInch(2)), 'Inch Scalar Multiplication Fail')

        self.assertAlmostEqual((oneMillimeter * 2), DimMillimeter(2), 5, 'Millimeter Scalar Multiplication Fail')
        self.assertEqual(type(oneMillimeter * 2), type(DimMillimeter(2)), 'Millimeter Scalar Multiplication Fail')

        self.assertAlmostEqual((oneMillimeter * 0), DimMillimeter(0), 5, 'Millimeter Scalar Multiplication Fail')
        self.assertEqual(type(oneMillimeter * 0), type(DimMillimeter(0)), 'Millimeter Scalar Multiplication Fail')

        self.assertAlmostEqual((oneMillimeter * -2), DimMillimeter(-2), 5, 'Millimeter Scalar Multiplication Fail')
        self.assertEqual(type(oneMillimeter * -2), type(DimMillimeter(-2)), 'Millimeter Scalar Multiplication Fail')


if __name__ == '__main__':
    unittest.main()
