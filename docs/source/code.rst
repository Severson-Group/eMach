Code Guidelines
-------------------------------------------

The documentation of the ``eMach`` repository contains sections devoted to ``analyzers`` and ``machines``. All of the documentation in the 
repository must be properly structured to ensure consistency as more contributors get added. This section contains the guidelines to detail the 
``code`` for each section of the ``eMach`` repository. 

Analyzer Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each analyzer within the ``eMach`` repository must be structured to analyze any set of ``user_inputs`` and produce accurate 
``user_outputs``. The code structure of each analyzer should contain each of the following classes:

1. DesignProblem Class
2. DesignAnalyzer Class

DesignProbelm Class
*******************************************

The ``DesignProblem`` class should contain all of the ``user_inputs`` and result in a single variable with multiple attributes that will be passed 
into the ``DesignAnalyzer`` class. The goal of this class is to take as many inputs as required by the ``user_inputs`` and process them into any and 
all required inputs of the ``DesignAnalyzer`` class. All input variables should be commented out and described as `attributes` of the problem class. 
The output of this class shall be used as a singular input of the following ``DesignAnalyzer`` class.

DesignAnalyzer Class
*******************************************

The ``DesignAnalyzer`` class is where all of the data processing required given the problem definition occurs. This class takes the problem variable
defined in the ``DesignProbelm`` class and uses various means of calculating, simulating, etc. to output raw data to be used in any post analyzers 
(per described in the ``Analyzer_Documentation`` section). All inputs of the problem class should be listed as `arguments`, which should at the very
least contain the defined problem. The outputs of the problem class should also be commented out in the code and described as `returns`. 

Machine Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each machine within the ``eMach`` repository must be structured to analyze any set of ``user_inputs`` to produce an accurate 
usable machine object. The code structure of each machine should contain each of the following code files:

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