# Unit Testing Guidelines for eMach Contributors

## Introduction
`To err is human`

It is imperative that humans are bound to make mistakes when writing their code, and it is often difficult to identify and review the issues in the code. Testing is a process of evaluating the software for bugs, thereby maintaining the quality of the code. There are [multiple types of testing methodology](https://www.geeksforgeeks.org/unit-testing-software-testing/) used in the software development environment.

This markdown document focuses on the [unit test methodology](https://en.wikipedia.org/wiki/Unit_testing) and discusses the testing guidelines to be followed by eMach contributors. Unit testing is the process of testing individual unit of code. The unit test framework for eMach is based on [unittest framework](https://docs.python.org/3/library/unittest.html). `unittest` is part of standard Python distribution, and therefore implementing the testing guidelines provided here does not require the installation of additional Python packages.

This document assumes that the reader is familiar with the unittest framework. However, if you are new to the unittest framework, this [introductory video](https://www.youtube.com/watch?v=6tNS--WetLI&ab_channel=CoreySchafer) is a great starting point.

## Defining Unit in Unit testing
It is often confusing what constitutes a "unit" in unit testing. eMach contributors should follow the `unit of work` concept discussed [here](https://livebook.manning.com/book/the-art-of-unit-testing-second-edition/chapter-1/16). The definition of `unit of work` is as follows,

`A unit of work is the sum of actions that take place between the invocation of a method in the system and a single noticeable end result by a test of that system. A noticeable end result can be observed without looking at the internal state of the system and only through its behavior. `

Hence, the unit of work can be a single method, or it can span multiple classes and functions.

The unit test file should test the unit of work, i.e. (`test_unit_of_work.py`). Test conditions and exceptions should be handled by test functions (`def test_condition`).

For example, `dimensions` in eMach implements arithmetic operations, unary operations, power, and nested operations. The unit of work, in this case, are individual functions (add, sub, etc.) that yield single noticeable results due to its invocation.

``` Python
def __add__(self, other): #<-- Unit of Work
    add = self._to_dimensionless() + other._to_dimensionless()
    self.result = add
    return type(self)._from_dimensionless(self)

def __sub__(self, other): #<-- Unit of Work
    sub = self._to_dimensionless() - other._to_dimensionless()
    self.result = sub
    return type(self)._from_dimensionless(self)
```

Based on the above example, separate files should be created to test `__add__` and `__sub__` functions.

## Guidelines on writing unit test
When writing unit tests, contributors are recommended to follow the guidelines discussed [here](https://docs.python-guide.org/writing/tests/).

A summary of the guidelines to be followed is provided below:
 - Unit test should test the smallest functionality.
 - Unit test should be fully independent.
 - Unit test should run fast.
 - Unit test should be readable (follow proper naming convention)n)

 ## Naming convention in writing unit test
 - Follow [PEP-8](https://www.python.org/dev/peps/pep-0008/) guidelines in naming the class and functions.
 - Python test modules should start with `test_` followed by the unit of work to be tested (ex: def test_add)
 - Test class should start with `Test` followed by the unit of work to be tested. (ex: class TestAdd)
 - Test functions should start with `test_` followed by the feature to be tested. (ex: def test_add_similar_dimlinear_objects).
More information about the naming convention for the unit test can be found over [here](https://dzone.com/articles/7-popular-unit-test-naming).


## Directory Structure
eMach contributors should place all the unit test files inside the `tests` folder. Appropriate subfolders should be used to organize the unit test files. An example folder structure specific to `dimensions` is shown below.
<!---Recommended practice on the directory layout is discussed [here](https://python.plainenglish.io/unit-testing-in-python-structure-57acd51da923). Sample directory layout specific to `dimensions` is as follows--->
```
eMach/ <-- Root Folder
├── model_obj
├── tools
└── tests/ <-- Test Folder
    └── dimensions/
        ├── test_add.py
        └── test_subtract.py
```

## How to write unit test using unittest framework
A brief tutorial on how to implement the unit test in python using [unittest framework](https://docs.python.org/3/library/unittest.html) is discussed [here](https://medium.com/swlh/introduction-to-unit-testing-in-python-using-unittest-framework-6faa06cc3ee1). A short script showing a barebones version of unittest implementation is as follows:

```Python
import unittest
class MyTestClass(unittest.TestCase): # Test Class
  def test_my_first_function(self): # Test Function
    pass
  def test_my_second_function(self): # Test Function
    pass
if __name__ == '__main__':
  unittest.main() # This will invoke all the test functions
```

An excerpt from `test_dim_linear_plus.py` is shown below, where a unit test case is written to test the addition of two dim_linear objects (`oneInch + oneInch`). The result is compared/asserted against the expected (`DimInch(2)`) for both the value and type using `assertAlmostEqual` and `assertEqual,` respectively. If the assertion is true, the test condition will pass and fail if it is false. A list of assertions supported by the unittest framework can be found [here](https://docs.python.org/3/library/unittest.html#assert-methods).

``` Python
"""
Library initialization
"""
import unittest

import model_obj
from model_obj.dimensions import DimInch, DimMillimeter

"""
Variables used for testing purpose
"""
oneInch = DimInch(1)
twoInches = DimInch(2)

oneMillimeter = DimMillimeter(1)
twoMillimeters = DimMillimeter(2)

"""
Test case
"""
class TestAddition(unittest.TestCase): # Test Class
    def test_single_dimension(self):
        val = oneInch + oneInch
        expected = DimInch(2)
        self.assertAlmostEqual(val, expected, 5)
        self.assertEqual(type(val), type(expected))
```
## How to run unit test using unittest framework
It is recommended to run the unit test using `Anaconda Prompt`,
1. Open `Anaconda Prompt` and navigate to `python\eMach` folder
2. Run the following command `python -m unittest discover -v`

This will run all the test cases under `python\eMach`. In order to run a specific test use `python -m unittest -v file_to_be_tested`. For example for testing `test_dim_linear_minus.py` the syntax should be `python -m unittest -v tests.dimensions.test_dim_linear_minus` (without the file extension). The file `test_dim_linear_minus.py` is under subfolder `dimensions` which is under `tests`.


## Conclusion
You are ready to write test conditions.
