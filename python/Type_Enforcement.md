### Type Enforcement ([JSON Schema](http://json-schema.org/understanding-json-schema/))
- Type hinting can be used to enforce the data type of the object. 
- Enforcement beyond datatype like the range of values, multiple of values(multiple of 2's and 3's), length of the string, length of the array, etc. can be done using [JSON Schema](https://pynative.com/python-json-validation/).

#### Example
```python
"""
JSON Schema Demo
"""
from jsonschema import validate
schema = {
# Schema is equivalent to specifying rules for the data.
    "type": "object",
    "properties": {
        "slots": {"type": "integer",
                  "multipleOf": 3,
                  "maximum": 48,
                  "minimum": 0},
        "poles": {"type": "integer",
                  "multipleOf": 2,
                  "maximum": 24,
                  "minimum": 2},
        "phase": {"type": "integer",
                  "maximum": 6,
                  "minimum": 3}
    },
}

def spp(dataum):
    print("Data Recieved")
    """
    Compute SPP
    """

toPass = {"slots": 12.0, "poles": 4.0, "phase": 3} #Data
try:
    validate(instance=toPass, schema=schema)  # Data type validation
    spp(toPass)
except Exception as e:
    print("Exception Occured")
    print(e)
```

In the above example, the function `spp` receives slots, poles, and phases data to compute slot per pole per phase. The Schema (rules) has been set to check whether the data is an integer, multiple of 3 in case of slots (2 in case of poles), and minimum and maximum limits. `validate` function will check for data violation based on rules specified in `schema`. 

If the data passed to the function is, 
```python
{"slots": 12.0, "poles": 4.0, "phase": 3}
```
The program will execute without errors. 

However, if the data passed to the function is 
```python
{"slots": 12.5, "poles": 5.0, "phase": 3}
```
or 
```python
{"slots": 52, "poles": 26, "phase": 7}
```
The program will throw an error as it violates the rules specified in `schema`. 
