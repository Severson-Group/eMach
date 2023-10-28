Code Guidelines
-------------------------------------------

Developers of eMach should read this document to understand expectations of code contributed to the eMach codebase. This document outlines the 
code requirements for ``analyzers`` and ``machine_designs``. Understanding of proper Python coding practices are necessary to contribute to each 
section of ``eMach``.

Analyzer Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each ``analyzer``  must be structured to analyze any set of user-defined inputs and produce user-defined outputs. The code 
structure of each ``analyzer`` should contain each of the following classes:

1. Design Problem Class
2. Design Analyzer Class

Design Problem Class
*******************************************

The Design Problem class shall contain an initializer and any definitions required of that initializer that accomplishes the following tasks:

1. Takes the user inputs as arguments
    a. Inputs are any and all information required to fully define a ``problem``
    b. This can include machine dimensions, data arrays, etc.
2. Comments out explanations of each argument, which should include the following:
    a. Arguemnt name
    b. A brief description of how it is used and where it is stored
    c. Argument units

Design Analyzer Class
*******************************************

The Design Analyzer class is where the data processing occurs after the problem has been initialized and should accomplish the following tasks:

1. Define an ``analyze`` function
    a. Argument should be a single problem object
    b. Return should be raw data that can be post-processed, if neccessary
2. Comments out explanations of each argument/return, which should include the following:
    a. Arguemnt/return name
    b. A brief description of how it is used and where it is stored
    c. Argument/return units

Machine Designs Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each ``machine_design`` must be structured to define a ``machine`` and ``machine_operating_point``. The code structure of 
each user-defined machine should contain each of the following code files:

1. Machine
2. Machine Operating Point

Machine
*******************************************

The ``machine`` code file shall contain a single class that contains several different definitions and properties. It should fully define a machine
by accomplishing the following tasks:

1. Defines the following dictionaries required by all machines:
    a. Dimensions
    b. Parameters
    c. Materials
    d. Winding
2. Checks if required inputs are present and, if necessary, notifies which ones are missing
3. Initializes ``machine`` object if required inputs are present and valid
4. Comments out explanations of each argument/return, which should include the following:
    a. Arguemnt/return name
    b. Argument/return type

Machine Operating Point
*******************************************

The ``machine_operating_point`` code file shall contain a single class defining a machine operating point by accomplishing the following tasks:

1. Initializes the operating point by taking user inputs as arguments
    a. Inputs are any and all information required to fully define a ``machine_operating_point``
    b. Defines required properties for initialization 
2. Comments out explanations of each argument, which should include the following:
    a. Arguemnt name
    b. A brief description of how it is used and where it is stored
    c. Argument units