Code Guidelines
-------------------------------------------

The documentation of the ``eMach`` repository contains sections devoted to ``analyzers`` and ``machine_designs``. All of the documentation in the 
repository must be properly structured to ensure consistency as more contributors get added. This section contains the guidelines to detail the 
``code`` for each section of the ``eMach`` repository. 

Analyzer Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each analyzer within the ``eMach`` repository must be structured to analyze any set of user-defined inputs and produce 
user-defined outputs. The code structure of each analyzer should contain each of the following classes:

1. DesignProblem Class
2. DesignAnalyzer Class

DesignProbelm Class
*******************************************

The ``DesignProblem`` class takes all of the user-defined inputs as its arguments. The output of the ``DesignProblem`` class is a single variable with 
multiple attributes. Once defined, the ``DesignProblem`` output variable is passed into the ``DesignAnalyzer`` class. The goal of the ``DesignProblem`` 
class is to take the user-defined inputs and process them into a single library that is usable by the ``DesignAnalyzer`` class. All attributes and 
results of the ``DesignProblem`` class should be explained in commented code that lists the variable definition and unit(s). The output of this class 
shall be used as an input of the following ``DesignAnalyzer`` class.

DesignAnalyzer Class
*******************************************

The ``DesignAnalyzer`` class is where all of the data processing required given the problem definition occurs. This class takes the problem variable
defined in the ``DesignProbelm`` class and uses various means of calculating, simulating, etc. to output raw data to be used in any post analyzers 
(per described in the ``Analyzer_Documentation`` section). All inputs of the problem class should be listed as `arguments`, which should at the very
least contain the defined problem. The outputs of the problem class should also be commented out in the code and described as `returns`. 

Machine Designs Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each machine design within the ``eMach`` repository must be structured to analyze any set of ``user_inputs`` to produce an 
accurate usable machine object. The code structure of each machine design should contain each of the following code files:

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

The ``machine_operating_point`` code file shall contain a single class, titled ``XXX_Machine_Oper_Pt``, that contains several different definitions 
and properties of the specific operating point that accomplish the following tasks:

1. Initializes the required operating point inputs
2. Defines each of the properties that result from the operating point