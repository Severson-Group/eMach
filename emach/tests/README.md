# Unit Test

This markdown document will explain about unit test framework in python and the recommended convention to be followed when implementing the unit test.

## How to write unit test using unittest framework
A brief tutorial on how to implement the unit test in python using [unittest framework](https://docs.python.org/3/library/unittest.html) is discussed [here](https://medium.com/swlh/introduction-to-unit-testing-in-python-using-unittest-framework-6faa06cc3ee1). A short script showing barebones version of unittest implenetation is as follows:

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

## Guidelines on writing Unit test
The contributors are recommended to follow the guidelines discussed [here](https://docs.python-guide.org/writing/tests/).

A summary of the guidelines include
 - Unit test should test the smallest functionality.
 - Unit test should be fully independent.
 - Unit test should run fast.
 - Unit test should be readable (follow proper naming convention)

## Directory Structure
Recommended practice on the directory layout is discussed [here](https://python.plainenglish.io/unit-testing-in-python-structure-57acd51da923). Sample directory layout is as follows,
```
eMach/ <-- Root Folder
├── model_obj
├── tools
└── tests/ <-- Test Folder
    └── dimensions/
        ├── test_add.py
        └── test_subtract.py
```

## Defining Unit in Unit testing
It is often confusing what constitutes unit in unit testing. eMach contributors should follow the `unit of work` concept discussed over [here](https://livebook.manning.com/book/the-art-of-unit-testing-second-edition/chapter-1/16). The Definition of `unit of work` is as follows,

`A unit of work is the sum of actions that take place between the invocation of a method in the system and a single noticeable end result by a test of that system. A noticeable end result can be observed without looking at the internal state of the system and only through its behavior. `

Hence by nature, the unit of work can be a single method, or it can span across multiple classes and functions.

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

## Naming convention in writing unit test
 - Follow [PEP-8](https://www.python.org/dev/peps/pep-0008/) guidelines in naming the class and functions. 
 - Python test modules should start with `test_` followed by the unit of work to be tested (ex: def test_add)
 - Test class should start with `Test` followed by the unit of work to be tested. (ex: class TestAdd)
 - Test functions should start with `test_` followed by the feature to be tested. (ex: def test_add_similar_dimlinear_objects). This is one of the [popular naming conventions](https://dzone.com/articles/7-popular-unit-test-naming) used in Agile Programming. 