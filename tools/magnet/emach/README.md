# Description

This document provides instructions to eMach contributers writing scripts for MagNet in Python.

# Getting Started

Before getting started, contributers should ensure that their systems are setup appropriately in order to interface Python with MagNet. A step by step procedure of the getting started with Python scripting for MagNet has been provided below:
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

MagNet APIs can be broadly classfied into 2 categories depending on the function signature: APIs which have output arguments and APIs which don't. The syntax for accessing the return values of both categories of APIS has been summarised below.
- APIs whose return values are not tied to an output argument can be directly called in Python. `makeSimpleCoil` is an example of such a function. Obtaining its return value in Python is as easy as: `coil = Doc.makeSimpleCoil(ProblemID, ArrayOfValues)`
- Accessing the return value of APIs with `Output Argument` functions can be more convoluted. The return values of some of these functions can be accessed similar to the prior example. One such API is `getFluxLinkageThroughCoil`. This API has 2 `output arguments` i.e, `magnitude` and `phase`. Its return values can be obtained with the following syntax: `magnitude, phase = Sol.getFluxLinkageThroughCoil(problem_id, 'Coil#1')`. 
However, using the above syntax format to certain APIs belonging to this category will not work. Implementations of this sort could result in a `com_error`. In order to access the return value of these functions, a VBScript wrapper of the same will have to be written in Python. `getParameter` is an example of a MagNet API whose return value can be accessed only via VBScript wrappers. The below code snippet illustrates the implementation of `getParamter` in Python:
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
