# Description

This document provides instructions to eMach contributers working with MagNet in Python.

# Getting Started

Before getting started, contributers should ensure that their systems are setup appropriately in order to interface Python with MagNet. A step by step procedure of getting started with Python scripting for MagNet has been provided below:
- In order for Python to communicate with MagNet, the pywin32 module has to be imported to call ActiveX compliant programs as Component Object Model (COM) automation servers. The pywin32 module comes with Anaconda3 installation and can be imported with the following command `from win32com.client import DispatchEx`
- The below example illustrates how handles to the MagNet scripting interface can be obtained in Python.
```python
   from win32com.client import DispatchEx 

   MN = DispatchEx("MagNet.Application") 
   MN.Visible = True #Makes MagNet window visible
   Doc = MN.newDocument()
   View = Doc.getView()
   Sol = Doc.getSolution()
   MNConsts = MN.getConstants() 
```
Running the above script should open a MagNet window on the user's system. If the Python console throws up a `ModuleNotFoundError`, please make sure that the path of the Anaconda3 site-packages has been added to the system's `Environment variables` as `PYTHONPATH`.
[This link goes through the steps of adding the PYTHONPATH for different platforms](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html)

# Function Returns

Functions in the MagNet API can be broadly classfied into two categories depending on the function signature: functions which have output arguments and funtions which do not. The syntax for accessing the return values of both categories of functions has been summarized below.
- Functions whose return values are not tied to an output argument can be directly called in Python. `makeSimpleCoil` is an example of such a function. Obtaining its return value in Python is as easy as: `coil = Doc.makeSimpleCoil(ProblemID, ArrayOfValues)`
- Functions that make use of output arguments to return data. Using these functions can be more convoluted. Certain functions of this type can be utilized similarly to the prior example. One such example is `getFluxLinkageThroughCoil`. This function has 2 `output arguments` specified in the MagNet documentation: `magnitude` and `phase`. The documentation specifies the VBScript syntax to use this function as `getFluxLinkageThroughCoil (solution ID, solver coil ID or name, magnitude, phase)`. In Python, this function can actually be called by treating the output arguments as return values, for example: `magnitude, phase = Sol.getFluxLinkageThroughCoil(problem_id, 'Coil#1')`.  
However, using the above syntax format is not compatible with all functions in this category and will throw a `com_error` when called in this manner. In order to utilize these functions, a VBScript wrapper must be written in Python. `getParameter` is an example of a MagNet function whose return value can be accessed only via VBScript wrappers. The below code snippet illustrates the implementation of `getParamter` in Python:
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
The function definition of MagNet APIs and their signatures can be obtained from MagNet's Help Topics.
[Click here to refer to the general Python example script provided by MagNet](https://support.sw.siemens.com/en-US/knowledge-base/MG611570)
