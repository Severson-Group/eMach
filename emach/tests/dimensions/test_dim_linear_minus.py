import unittest


from eMach.python.emach.model_obj import DimInch, DimMillimeter

oneInch = DimInch(1)
twoInches = DimInch(2)
elevenInches = DimInch(11)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)
fiftyMillimeters = DimMillimeter(50)
two54Millimeters = DimMillimeter(254)


class TestSubtraction(unittest.TestCase):
    def test_single_dimension(self):
        self.assertAlmostEqual((oneInch - oneInch), DimInch(0), 5, 'Inch Subtraction Fail')
        self.assertEqual(type(oneInch - oneInch), type(oneInch), 'Inch Subtraction Fail')

        self.assertAlmostEqual((twoInches - oneInch), DimInch(1), 5, 'Inch Subtraction Fail')
        self.assertEqual(type(twoInches - oneInch), type(twoInches), 'Inch Subtraction Fail')

        self.assertAlmostEqual((oneMillimeter - oneMillimeter), DimMillimeter(0), 5, 'Millimeter Subtraction Fail')
        self.assertEqual(type(oneMillimeter - oneMillimeter), type(oneMillimeter), 'Millimeter Subtraction Fail')

        self.assertAlmostEqual((twoMillimeters - oneMillimeter), DimMillimeter(1), 5, 'Millimeter Subtraction Fail')
        self.assertEqual(type(twoMillimeters - oneMillimeter), type(twoMillimeters), 'Millimeter Subtraction Fail')

    def test_different_dimension(self):
        self.assertAlmostEqual((elevenInches - two54Millimeters), DimInch(1), 5, 'Inch-Millimeter Subtraction Fail')
        self.assertAlmostEqual(type(elevenInches - two54Millimeters), type(elevenInches), 5, 'Inch-Millimeter '
                                                                                             'Subtraction Fail')

        self.assertAlmostEqual((fiftyMillimeters - oneInch), DimMillimeter(24.6), 5, 'Millimeter-Inch Subtraction Fail')
        self.assertAlmostEqual(type(fiftyMillimeters - oneInch), type(fiftyMillimeters), 5, 'Millimeter-Inch '
                                                                                            'Subtraction Fail')

        self.assertAlmostEqual((elevenInches - two54Millimeters - oneInch), DimInch(0), 5,
                               'Inch-Millimeter-Inch Subtraction Fail')
        self.assertAlmostEqual(type(elevenInches - two54Millimeters - oneInch), type(elevenInches), 5,
                               'Inch-Millimeter-Inch Subtraction Fail')

        self.assertAlmostEqual((fiftyMillimeters - twoInches), DimMillimeter(-0.8), 5, 'Millimeter-Inch Subtraction '
                                                                                       'Fail')
        self.assertAlmostEqual(type(fiftyMillimeters - twoInches), type(fiftyMillimeters), 5,
                               'Millimeter-Inch Subtraction Fail')


if __name__ == '__main__':
    unittest.main()
