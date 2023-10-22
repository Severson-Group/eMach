Code Guidelines
-------------------------------------------

Developers of eMach should read this document to understand expectations of code contributed to the eMach codebase. This document outlines the 
code requirements for ``analyzers`` and ``machine_designs``. Understanding of proper Python coding practices are necessary to contribute to each 
section of ``eMach``.

Analyzer Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each ``analyzer`` within the ``eMach`` repository must be structured to analyze any set of user-defined inputs and produce 
user-defined outputs. The code structure of each ``analyzer`` should contain each of the following classes:

1. DesignProblem Class
2. DesignAnalyzer Class

DesignProbelm Class
*******************************************

The ``DesignProblem`` class takes all of the user-defined inputs as its arguments. The output of the ``DesignProblem`` class is a single variable with 
multiple attributes. The code for each input variable must clearly defined the input variable and add it as an attribute of the `self` variable within 
each ``DesignProblem`` class. The output of the ``DesignProblem`` class is the single `self` variable with as many attributes as desired. Commented out
within the class should be explanations of each input variable. This should include the variable name, a brief description of the variable, and the 
units of that variable. The output of the ``DesignProblem`` class is then used by the ``DesignAnalyzer` class.

DesignAnalyzer Class
*******************************************

The ``DesignAnalyzer`` class is where all of the data processing required given the problem definition occurs. This class takes the singular output 
variable from the ``DesignProbelm`` class defined as `problem: XXXProbelm`. The `XXX` term should be the title of the analyzer. Commented out within 
the ``DesignAnalyzer`` class should be each of it's input arguments and output returns. The commented code should contain the variable named, brief 
descriptions of the variables, and variable units split between `arguments` and `returns` sections.

Machine Designs Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each ``machine_design`` within the ``eMach`` repository must be structured to define both a parameterized ``machine`` and a 
parameterized ``machine_operating_point``. The code structure of each user-defined machine should contain each of the following code files:

1. Machine
2. Machine Operating Point

Machine
*******************************************

The ``machine`` code file shall contain a single class, titled ``XXX_Machine``, that contains several different definitions and properties that 
accomplish the following tasks:

1. Initializes the dimensions, parameters, materials, and winding
2. Defines required inputs from input libraries
3. Checks if all inputs are present and, if necessary, notifies which ones are missing
4. Defines all necessary machine properties based on machine inputs

Machine Operating Point
*******************************************

The ``machine_operating_point`` code file shall contain a single class, titled ``XXX_Machine_Oper_Pt`` that contains several different definitions 
and properties of the specific operating point that accomplish the following tasks:

1. Initializes the required operating point inputs
2. Defines each of the properties that result from the operating point