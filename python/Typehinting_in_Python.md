# Typehinting in Python



[Type hinting](https://www.python.org/dev/peps/pep-0484/) is a formal solution to statically indicate the type of a value within your Python code. [1]

Traditionally python is a [dynamically typed language](https://android.jlelse.eu/magic-lies-here-statically-typed-vs-dynamically-typed-languages-d151c7f95e2b); however, to improve project organization and inherit the advantages of static typed language, type hinting was introduced in Python 3.5. 

### Why Type hints? [2]
- Build and maintain a clean architecture.   
- Serves as code documentation. 

### Typehint implementation in Python
##### Example  


``` python
def spaceoddity(name):
   return "Ground Control to " + name
```

In the above example, `def spaceoddity` receives a string, concatenates it to another string, and returns the resultant string. Here type hinting can be implemented when receiving the string and returning the string. 

```python
def spaceoddity(name: str) -> str:
   return "Ground Control to " + name
```
`name:str` indicates that the input argument should be a string,  `->str` indicates the `spaceoddity` function will return string. 


### Type Checking in Python
Type checking is a [static typed language](https://android.jlelse.eu/magic-lies-here-statically-typed-vs-dynamically-typed-languages-d151c7f95e2b) technique used to verify the type safety of the program. 
- Most Modern IDE has inbuilt type checkers. 
- There are external static type checkers, and one of the most popular ones is [mypy](http://mypy-lang.org/).
- If a type hint is implemented in the code, the type checker can check for the violation before runtime. 

 
# Reference Materials
[1] : [Real Python Type Hinting](<https://realpython.com/lessons/type-hinting/>)
[2] : [Pros and Cons of Type Hints](<https://realpython.com/lessons/pros-and-cons-type-hints/#:~:text=Type%20hints%20improve%20IDEs%20and,the%20types%20in%20your%20program.>) 

