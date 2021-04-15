##What is Unit test?

A unit test is a way of testing a unit - the smallest piece of code that can be logically isolated in a system.

##Unit Testing in Python
There are many unit testing framework in python.
Most commonly used are [Unittest](https://docs.python.org/3/library/unittest.html) and  [Pytest](https://docs.pytest.org/en/stable/).
Unittest is built in within python distribution (like numpy).
Pytest needs to be installed (Pytest comes preinstalled in conda distribution).
Both have the same functionality but the way you write the code will be different.
This markdown document will explain how to build and run unit tests using [Unittest](https://docs.python.org/3/library/unittest.html) framework.

##Unittest framework - Bare Minimum


To use the unittest framework we need to import unittest library,
``` python
import unittest
```

To invoke all the test cases,
```python
if __name__ == '__main__':
    unittest.main()
```

A test class needs to be created which will inherit `unittest.TestCase`
```python
class MyTestCase(unittest.TestCase):
  #This class will contain my test functions

```
Test case function should be written inside the test class,
It is mandatory that the test case function **should** be prefixed with `test_`
for the unittest framework to consider the test function.
```python
class MyTestCase(unittest.TestCase):

  def test_my_function(self):
    #Unittest framework will run the testcase
    pass

  def my_test_case(self):
    """
    Unittest framework will not run this testcase
    as the test function doesn't begin with test_
    """
    pass
```
Test class may contain multiple testcases based on the project structure,
```python
class MyTestCase(unittest.TestCase):

  def test_my_first_function(self):
    pass

  def test_my_second_function(self):
    pass
```
Putting together all the pieces the bare minimum test case code should be as follows,

```Python
import unittest

class MyTestCase(unittest.TestCase):

  def test_my_first_function(self):
    pass

  def test_my_second_function(self):
    pass

if __name__ == '__main__':
  unittest.main()
```

##Write your unit test
Before writing our first unit test we need to understand the [AAA model](https://medium.com/swlh/introduction-to-unit-testing-in-python-using-unittest-framework-6faa06cc3ee1) of writing unit test.
AAA Model stands for Arrange, Act and Assert.

##### Arrange: Initializing variables/function to the function under the test.

##### Act:  Run the function under the test.

##### Assert : Check whether the code is running as expected.

```python
import unittest

def sum(lhs, rhs):
  #Function Under test
  my_output = lhs + rhs
  return my_output

class MyTestCase(unittest.TestCase):
  def test_function_under_test(self):
    # Arrange : Initialize variables
    lhs = 10
    rhs = 20
    # Act
    output = sum(lhs, rhs)
    # Assert
    self.assertEqual(output, lhs+rhs)

if __name__ == '__main__':
  unittest.main()
```

In the above code snippet we are checking the functionality of the function `sum`,
We are implementing AAA model by arranging our inputs `lhs` and `rhs`, acting on it by
passing out inputs to the function under the test and finally asserting by checking the
function output and `lhs+rhs` using `assertEqual`. List of commonly used assert functions can be found [here.](https://docs.python.org/3/library/unittest.html#assert-methods).

##Running Unittest
A recomended way to run unittest is to run it from terminal.
1. Navigate to the working folder
2. Run `python -m unittest discover -v`

##More Reads
1. [Official unittest documentation](https://docs.python.org/3/library/unittest.html#module-unittest)
2. [Testing in Python](https://realpython.com/python-testing/)
