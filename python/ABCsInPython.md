# Background

One of the key features of object-oriented-programming is inheritance. Inheritance is the way by which a class can take (or inherit) properites of another class. Utilizing inheritance to 
its full capability paves the way to the creation of modular and easily extensible code. Inheritance can also be employed in order to specify "contracts" which child classes must uphold. 
Abstract base classes (`ABC`) provide a way of enforcing these contracts. 

# Abstract Base Classes in Python

ABCs can be employed in Python by using the in-built `abc` module, introduced back in 2007 with [PEP 3119](https://www.python.org/dev/peps/pep-3119/). 
The below code provides an example of abstract base class implementation in Python.

```python
from abc import ABC, abstractmethod

class Book(ABC):
    
    @abstractmethod
    def author(self):
        pass
    
    @abstractmethod
    def number_of_pages(self):
        pass
```

In the above example, Book has been defined as an abstract base class with `author` and `number_of_pages` decalred as its abstract methods using the `@abstractmethod` decorator. Any class inheriting `Book` has to uphold the contract as specified by the class, i.e. they must have `author` and `number_of_pages` among their attributes. The below code snippet illustrates a child class of `Book` which does not implement the abstract methods specified by the parent class. Upon instantiating the class, Python raises a `TypeError`.

```python
class HitchikersGuideToTheGalaxy(Book):
    
    def aliens_in_book(self):
        return 'Yes!'

x = HitchikersGuideToTheGalaxy()

TypeError: Can't instantiate abstract class HitchikersGuideToTheGalaxy with abstract methods author, number_of_pages
```

An example of a properly defined child class of `Book` is provided below. As can be observed, this class implements both `author` and `number_of_pages` methods and therefore upholds the contract as specified by `Book`.

```python
class FoucaultsPendulum(Book):
    
    def author(self):
        return 'Eco, Umberto'
    
    def number_of_pages(self):
        return 640
    
    def aliens_in_book(self):
        return 'No...'
```

# References
[1] : [Abstract Base Classes - The Python Standard Library](https://docs.python.org/3/library/abc.html)

[2] : [Abstract Base Classes - Learn Python Programming](https://pythonprogramminglanguage.com/abstract-base-classes/)

[3] : [Abstract base classes and how to use them in your data science project](https://towardsdatascience.com/abstract-base-classes-and-how-to-use-them-in-your-data-science-project-2503c13704f4) 

