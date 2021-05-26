# Unit Test

This markdown document will explain about unit test framework in python and the recommended convention to be followed when implementing the unit test.

## How to write unit test using unittest framework
A brief tutorial on how to implement the unit test in python using [unittest framework](https://docs.python.org/3/library/unittest.html) is discussed [here](https://medium.com/swlh/introduction-to-unit-testing-in-python-using-unittest-framework-6faa06cc3ee1). A short script showing barebones version of unittest implenetation is as follows:

```Python
import unittest
class MyTestCase(unittest.TestCase): # Test Class
  def test_my_first_function(self): # Test Function
    pass
  def test_my_second_function(self): # Test Function
    pass
if __name__ == '__main__':
  unittest.main() # This will invoke all the test functions
```

## Guidelines on writing Unit test
The contributors are recomended to follow the guidelines discussed [here](https://docs.python-guide.org/writing/tests/).

A brief summary of the guidelines include
 - Unit test should test the smallest functionality.
 - Unit test should be fully independent.
 - Unit test should run fast.
 - Unit test should be readable (follow proper naming convention)

## Directory Strucutre
Recommended practice on the directory layout is discussed [here](https://python.plainenglish.io/unit-testing-in-python-structure-57acd51da923). Sample directory layout is as follows,
```
eMach/
├── model_obj
├── tools
└── tests/
    └── dimensions/
        ├── test_add.py
        └── test_subtract.py
```
## Naming convention in writing unit test
Python test functions should start with `test_` followed by the test
