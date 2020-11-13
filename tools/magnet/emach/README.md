# Desciption

This document is aimed at helping users write scripts for MAGNET in python.

# Setup

- In order for python to communicate with MAGNET, the pywin32 module has to be imported to call ActiveX compliant programs as Component Object Model (COM) automation servers. The pywin32 module comes with the Anaconda3 installation and can be imported with the command `from win32com.client import DispatchEx`
- If the importing of the module raises an error flag, please make sure that the path of the Anaconda3 site-packages has been added to the system's `Environment variables` as `PYTHONPATH`.
[This link goes through the steps of adding the PYTHONPATH for different platforms](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html)
- The below example illustrates how handles to the MAGNET scripting interface can be obtained in python
```python
   from win32com.client import DispatchEx 

   MN = DispatchEx("MagNet.Application") 
   MN.Visible = True #Makes MAGNET window visible
   Doc = MN.newDocument()
   View = Doc.getView()
   Sol = Doc.getSolution()
   MNConsts = MN.getConstants() 
```
# Function Returns

MAGNET APIs can be divided into 2 categories based on how the function's return value can be accessed:
- Functions who's return values can be directly accessed by assigining the function call to a variable fall under the first category. `makeSimpleCoil` is an example of such a function. Its return value can be obtained in python directly with the following syntax: `coil = Doc.makeSimpleCoil(ProblemID, ArrayOfValues)`
- Functions who's return values can be accessed only via an `Output Argument` fall under the second category. Since python does not natively support ouput arguments in its function calls, the return values of these functions can be accessed only by writing a VBScript wrapper of the function in python. The below code snippet illustrates the implementation of one such function, 'getParameter()' in python:
```python
    MN.processCommand("REDIM strArray(0)")
    MN.processCommand("DIM pType")
    MN.processCommand("pType = getDocument.getParameter(\"{}\", \"{}\", strArray)".format(path,parameter))
    MN.processCommand('Call setVariant(0, strArray,"PYTHON")')    
    param = MN.getVariant(0,"PYTHON")
    MN.processCommand('Call setVariant(0, pType,"PYTHON")')    
    param_type = MN.getVariant(0,"PYTHON")
    return param, param_type
```
The function definition of MAGNET APIs can be obtained from MAGNET's Help Topics.

