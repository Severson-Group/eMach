Documentation Guidelines
-------------------------------------------

The documentation of the ``eMach`` repository contains sections devoted to ``analyzers`` and ``machines``. All of the documentation in the 
repository must be properly structured to ensure consistency as more contributors get added. This section contains the guidelines to detail the 
``documentation`` for each section of the ``eMach`` repository. 

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
section. This can be in the form of equations, images, explanations, etc. Any assumptions that are made must be fully explained in this section and 
any publications that are referenced in the background information or analyzer code should be included here.

User Inputs
*******************************************

The ``user_inputs`` section of the analyzer needs to divulge to the user what is required as inputs to the analyzer. This should come in the form of 
organized tables, example code, and any other required inputs that the user must provide to the analyzer. If additional images are required to understand
the extent of the analyzer, they should be included here. The tables included in this section must document the input variables, and should come in the 
form of 3 columns. The columns should be listed as the input variables, the units of the input variables, and a short description of each input variable.
The example code contained in this section should be the code that will run with the necessary inputs, and that results in the outputs documented in the 
following section.

User Outputs
*******************************************

The ``user_outputs`` section should contain the outputs that will result from running the code mentioned in the ``user_inputs`` section. This section
should contain similar tables, code, and any other post-processing that will be useful for a proper understanding of the analyzer. Any plots that are 
shown as a result of this analyzer should be included in this section as well. The output table should contain the same form as the input table. The 
code that should be included in this section is any post-processing code to calculate the final variables or construct any plots. This code should not
be the analyzer code itself, but any code that is required to post-process the analyzer outputs to usable data or images. 

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
fully explained in this section and any publications that are referenced in any of the background information or machine code should be included here.

Inputs from User
*******************************************

The ``user_inputs`` section of the machine needs to explain to the user what is required as inputs to the machine. This should come in the form the 
following four dictionaries/libraries:

1. Dimensions
2. Parameters
3. Materials
4. Winding

The ``dimensions`` section of the machine must detail any and all dimensions of the stator and rotor configuration. The documentation in this subsection
should come in the form of organized tables, example code, and an image of the parameterized cross sections. If additional information is necessary to 
understand the extent of the machine dimensions, it should be included here. The tables included in this section document the machine dimensions, and 
should follow the form of the previous ``user_inputs`` and ``user_outputs`` tables. The example code contained in this section should be the code that 
will be used by the machine evaluator file.

The ``parameters`` section of the machine needs to divulge to the user the parameters of the machine configuration. Items such as pole pairs, slots, 
names, rated conditions, etc. should be included here. The documentation of this subsection should come in the form of organized tables and example 
code. If additional information is necessary to understand the extent of the machine parameters, it should be included here. The table included in this 
section should follow the form of the previous ``dimensions`` table. The example code contained in this section should be the code that will be used by 
the machine evaluator file.

The ``materials`` section of the machine must explain the materials used in the machine configuration. The documentation in this subsection should 
come in the form of tables and example code containing the materials for, at the very least, the stator, rotor, coils, shaft, and air. If additional 
information is necessary to understand the extent of the materials, it should be included here. The table included in this section should follow the 
form of the previous ``parameters`` table. The example code contained in this section should be the code that will be used by the machine evaluator file.

The ``winding`` section of the machine should detail the properties of the machine winding configuration. The documentation in this subsection should 
come in the form of tables, winding diagrams, and example code. If additional information is necessary to understand the extent of the winding, it 
should be included here. The table included in this section should follow the form of the previous ``materials`` table. The example code contained in 
this section should be the code that will be used by the machine evaluator file.

Creating a Machine Object
*******************************************

All of the ``user_inputs`` libraries/dictionaries must be read and constructed into a callable object. This is done by transforming the inputs 
into the ``machine`` object that is described in the ``Machine_Code`` section. This section should include example code taking the four input 
libraries/dictionaries and passing them into a ``machine`` object for a given machine type.

Operating Point Inputs
*******************************************

The ``operating_point_inputs`` section of the machine documentation needs to divulge to the user what is required as inputs to define the machine 
operating point. This should come in the form of an organized table. The table must document the input variables that are defined in the code for 
each different machine type. The table should be in the same form as all of the other tables included in the previous sections. The example code 
contained in this section should be the code that will be used by the machine evaluator file.

Creating a Machine Operating Point Object
*******************************************

The ``machine_operating_point`` section of the machine documentation must detail what code is required to define the machine operating point object.
This should come in the form of organized and commented code. The example code contained in this section should be the code that will be used by the 
machine evaluator file.