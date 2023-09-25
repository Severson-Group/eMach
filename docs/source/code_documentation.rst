Code/Documentation Guidelines
-------------------------------------------

The docuemntation of the ``eMach`` repository contains sections devoted to ``analyzers`` and ``machines``. All of the documentation in the 
repository must be properly structured to ensure consistency as more contributors get added. This section contains the guidelines to document the 
``code`` and ``documentation`` for each section of the ``eMach`` repository. 

Analyzer Documentation
++++++++++++++++++++++++++++++++++++++++++++

Each analyzer within the ``eMach`` codebase must be summarized such that someone with a basic understanding of electric machines can understand the
purpose and structure of the analyzer. This is summarized in a form that contains the following subsections:

1. Model Background
2. User Inputs
3. User Outputs

Model Background
*******************************************

The ``model_background`` section needs to provide information to explain the motivation, application, and any other knowledge required to understand
where and why the analyzer is being applied. The entirety of the background information for each ``eMach`` analyzer must be fully explained in this 
section. This can be in the form of equations, images, explanations, etc. Any assumptions that are made must be fully explained in this section as 
well as any publications that are referenced in any of the background information or analyzer code should be included here.

User Inputs
*******************************************

The ``user_input`` section of the analyzer needs to divulge to the user what is required as an input to the analyzer. This should come in the form of 
organized tables, example code, and any other required input that the user must provide to the analyzer. If additional images are required to understand
the extent of the analyzer, they should be included here. The tables included in this section must document the input variables, and should come in the 
form of 3 columns. The column should be listed as the input variable, the units of the input variable, and a short description of each input variable.
The example code contained in this section should be the code that will run with the necessary inputs, that results in the outputs documented in the 
following section.

User Outputs
*******************************************

The ``user_outputs`` section should contain the outputs that will result from running the code mentioned in the ``user_inputs`` section. This section
should contain similar tables, code, and any other post-processing that will be useful for a proper understanding of the analyzer. Any plots that are 
shown as a result of this analyzer should be included in this section as well. The output table should contain the same form as the input table. The 
code that should be included in this section is any post-processing code to calculate the final variables or construct any plots. This code should not
be the analyzer code itself, but any code that is required to post-process the analyzer outputs to usable data or images. 

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

Machine Documentation
++++++++++++++++++++++++++++++++++++++++++++

Each machine within the ``eMach`` codebase must be summarized such that the purpose and structure of how each machine is defined, constructed, and 
created can be understood. This is summarized in a form containing the following subsections:

1. Machine Background
2. User Inputs
3. Creating a Machine Object
4. Operating Point Inputs
5. Creating a Machine Operating Point Object

Machine Background
*******************************************

The ``machine_background`` section needs to provide information to explain the motivation, application, and any other knowledge required to understand
where and why the machine is being applied. This can be in the form of equations, images, explanations, etc. Any assumptions that are made must be 
fully explained in this section as well as any publications that are referenced in any of the background information or machine code.

Inputs from User
*******************************************

The ``user_input`` section of the machine needs to explain to the user what is required as an input to the machine. This should come in the form the 
following four dictionairies/libraries:

1. Dimensions
2. Parameters
3. Materials
4. Winding

The ``dimensions`` section of the machine must detail any and all dimensions of the stator and rotor configuration. The documentation in this subsection
should come in the form of organized tables, example code, and an image of the parameterized cross sections. If additional information is necessary to 
understand the extent of the machine dimensions, it should be included here. The tables included in this section document the machine dimensions, and 
should follow the form of the previous ``user_inputs`` and ``user_outputs`` tables. The example code contained in this section should be the code that 
will be used by the machine evaluator file.

The ``parameters`` section of the machine needs to divulge to the parameters of the machine configuration. Items such as pole pairs, slots, names, rated
conditions, etc. should be included here. The documentation of this subsection should also come in the form of organized tables and example code. If 
additional information is necessary to understand the extent of the machine parameters, it should be included here. The table included in this section 
should follow the form of the previous ``dimensions`` table. The example code contained in this section should be the code that will be used by the 
machine evaluator file.

The ``materials`` section of the machine must explain the materials used in the machine configuration. The documentation in this subsection should 
come in the form of tables and example code containing the materials for the stator, rotor, coils, shaft, and air. If additional information is necessary 
to understand the extent of the materials, it should be included here. The table included in this section should follow the form of the previous 
``parameters`` table. The example code contained in this section should be the code that will be used by the machine evaluator file.

The ``winding`` section of the machine should detail the properties of the machine winding configuration. The documentation in this subsection should 
come in the form of tables, winding diagrams, and example code. If additional information is necessary to understand the extent of the winding, it 
should be included here. The table included in this section should follow the form of the previous ``materials`` table. The example code contained in 
this section should be the code that will be used by the machine evaluator file.

Creating a Machine Object
*******************************************

The ``user_inputs`` in the form of libraries/dictionaries must be read and constructed into a callable object. This is done by transforming the inputs 
into the ``machine`` object that is described in the following ``Machine_Code`` section. This section should include example code taking the four
input libraries/dictionaries and passing them into a ``machine`` object for a given machine type.

Operating Point Inputs
*******************************************

The ``operating_point_input`` section of the machine documentation needs to divulge to the user what is required as an input to define the machine 
operating point. This should come in the form of an organized table. The table must document the input variables that are defined in the code for 
each different machine type. The table should be in the same form as all of the other tables included in the previous sections. The example code 
contained in this section should be the code that will be used by the machine evaluator file.

Creating a Machine Operating Point Object
*******************************************

The ``machine_operating_point`` section of the machine documentation must detail what code is required to define the machine operating point object.
This should come in the form of organized and commented code. The example code contained in this section should be the code that will be used by the 
machine evaluator file.

Machine Code
++++++++++++++++++++++++++++++++++++++++++++

The code required for each machine within the ``eMach`` repository must be structured to analyze any set of ``user_inputs`` to produce an accurate 
usable machine object. The code structure of each machine should contain each of the following code files:

1. Machine
2. Machine Operating Point

Machine
*******************************************

The ``machine`` code file shall contain a single class that contains several different definitions and properties that accomplish the following tasks:

1. Initializes the dimensions, parameters, materials, and winding
2. Defines required inputs from input libraries
3. Checks if all inputs are present and, if necessary, notifies which ones are missing
4. Defines all necessary machine properties based on machine inputs

Machine Operating Point
*******************************************

The ``machine_operating_point`` code file shall contain a single class that contains several different definitions and properties of the specific 
operating point that accomplish the following tasks:

1. Initializes the required operating point inputs
2. Defines each of the properties that result from the operating point