
import unittest
from eMach.python.emach.model_obj.dimensions import DimMillimeter, DimInch, DimDegree, DimRadian



oneInch   = DimInch(1)
twoInches = DimInch(2)
threeInches = DimInch(3)

oneMillimeter  = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)
threeMillimeters = DimMillimeter(3)



class MyTestCase(unittest.TestCase):
    def test_single_dimension(self):
        self.assertEqual(round(oneInch+twoInches), threeInches)
        self.assertEqual(type(oneInch + twoInches), type(oneInch))


if __name__ == '__main__':
    unittest.main()
