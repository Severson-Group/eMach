import unittest


from eMach.python.emach.model_obj import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)


oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)



class TestAddition(unittest.TestCase):
    def test_single_dimension(self):
        self.assertAlmostEqual((oneInch + oneInch), DimInch(2), 5, 'Inch Addition Fail')
        self.assertEqual(type(oneInch + oneInch), type(DimInch(2)), 'Inch Addition Fail')

        self.assertAlmostEqual((oneInch + twoInches), DimInch(3), 5, 'Inch Addition Fail')
        self.assertEqual(type(oneInch + twoInches), type(DimInch(3)), 'Inch Addition Fail')

        self.assertAlmostEqual((oneMillimeter + oneMillimeter), DimMillimeter(2), 5, 'Millimeter Addition Fail')
        self.assertEqual(type(oneMillimeter + oneMillimeter), type(DimMillimeter(2)), 'Millimeter Addition Fail')

        self.assertAlmostEqual((oneMillimeter + twoMillimeters), DimMillimeter(3), 5, 'Millimeter Addition Fail')
        self.assertEqual(type(oneMillimeter + twoMillimeters), type(DimMillimeter(3)), 'Millimeter Addition Fail')

    def test_different_dimension(self):
        self.assertAlmostEqual((oneInch + oneMillimeter), DimInch(1.0393701), 5, 'Inch+Millimeter Addition Fail')
        self.assertAlmostEqual(type(oneInch + oneMillimeter), type(DimInch(1.0393701)), 5, 'Inch+Millimeter Addition '
                                                                                           'Fail')

        self.assertAlmostEqual((oneMillimeter + oneInch), DimMillimeter(26.4), 5, 'Millimeter+Inch Addition Fail')
        self.assertAlmostEqual(type(oneMillimeter + oneInch), type(DimMillimeter(26.4)), 5, 'Millimeter+Inch Addition '
                                                                                            'Fail')

        self.assertAlmostEqual((oneInch + oneMillimeter + oneMillimeter), DimInch(1.0787402), 5,
                               'Inch+Millimeter+Millimeter Addition Fail')
        self.assertAlmostEqual(type(oneInch + oneMillimeter + oneMillimeter), type(DimInch(1.0787402)), 5,
                               'Inch+Millimeter+Millimeter Addition Fail')

        self.assertAlmostEqual((twoMillimeters + twoInches), DimMillimeter(52.8), 5, 'Millimeter+Inch Addition Fail')
        self.assertAlmostEqual(type(twoMillimeters + twoInches), type(twoMillimeters), 5,
                               'Millimeter+Inch Addition Fail')


if __name__ == '__main__':
    unittest.main()
