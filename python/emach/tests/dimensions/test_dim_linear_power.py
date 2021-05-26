import unittest

import model_obj
from model_obj.dimensions import DimInch, DimMillimeter

oneInch = DimInch(1)


class TestPower(unittest.TestCase):
    def test_fail_conditions_power(self):
        with self.assertRaises(Exception):
            oneInch ** 2

        with self.assertRaises(Exception):
            2 ** oneInch

        with self.assertRaises(Exception):
            oneInch ** oneInch


if __name__ == '__main__':
    unittest.main()
