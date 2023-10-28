Documentation Guidelines
-------------------------------------------

Developers of eMach should read this document to understand expectations of the documentation files related to any code contributed to the eMach 
codebase. This document outlines the requirements for the documentation sections related to ``analyzers`` and ``machine_designs``.

Analyzer Documentation
++++++++++++++++++++++++++++++++++++++++++++

Each analyzer within the ``eMach`` codebase must be summarized such that someone with a basic understanding of electric machines can understand the
purpose and structure of the analyzer. The documentation files devoted to each analyzder must contain the following sections:

1. Model Background
2. Inputs from User
3. Outputs to User

Model Background
*******************************************

The model background section needs to provide information to explain the motivation, application, and any other knowledge required to understand
where and how the analyzer is being applied. All relevant background information for each analyzer must be fully explained in this section. This 
can be in the form of equations, images, explanations, etc. Any assumptions that are made must be fully explained in this section and any 
publications that were referenced should be included here as well.

Input from User
*******************************************

The user inputs section of each analyzer needs to explain to the user what is required as inputs to the analyzer. At minimum, a table must be 
provided to explain to the user what is needed as inputs. The table must include three columns, organized like the following:

1. Arguments
2. Descriptions
3. Units (if necessary)

If necessary or desired, example code can be included for the user after the table is presented. If additional is required to understand the inputs
of the analyzer, it needs to also be included in this section.

Output to User
*******************************************

The user outputs section of each analyzer needs to contain the outputs that will result from running the analyzer code given the user inputs described
in the previous section. The output should be include at minimum a table of the output variables. Generally, the output table should be a table 
constructed with the following columns:

1. Returns
2. Descriptions
3. Units (if necessary)

If any output code or images result from the analyzer, they must be included in this section. If post-processing code is necessary to further understand
the output of the analyzer, it must be included in this section as well. The analyzer code itself is `not` included at all in the analyzer documentation.

Machine Designs Documentation
++++++++++++++++++++++++++++++++++++++++++++

Each machine within the ``eMach`` codebase must be similarly summarized such that the purpose and structure of how each machine is defined, constructed, 
and operated can be understood. This is summarized in a form containing the following sections:

1. Machine
    a. Machine Background
    b. Inputs from User
    c. Creating a Machine Object
2. Machine Operating Point
    a. Inputs from User
    b. Creating a Machine Operating Point Object

Machine Background
*******************************************

The machine background section needs to provide information to explain the motivation, application, and any other knowledge required to understand
where and how the machine is being applied. All relevant background information for each machine must be fully explained in this section. This 
can be in the form of equations, images, explanations, etc. Any assumptions that are made must be fully explained in this section and any 
publications that were referenced should be included here.

Machine Inputs from User
*******************************************

The user inputs section of the machine needs to explain to the user what is required as inputs to the machine. This should come in the form the 
following four dictionaries/libraries, each contained in their own subsection:

1. Dimensions
2. Parameters
3. Materials
4. Winding

The documentation for each subsection must contain a description/explanation of the details behind how each applies to their respective machine. 
Additional information for each subsection should come in the form of example code and tables. The example code should mirror code that should
be placed in the machine evaluation example folders located `here <https://github.com/Severson-Group/eMach/tree/develop/examples/mach_eval_examples>`__. 
Each table should be laid out with the following column structure:

1. Keys
2. Descriptions
3. Units (if necessary)

Specific requirements that must be included in the documentation for the four dictionaries/libraries can be seen here:

1. Dimensions section
    a. Parameterized cross-sections
4. Winding
    a. Winding layout/stator diagram

Creating a Machine Object
*******************************************

All of the user input dictionaries/libraries must be read and constructed into a callable object. This is done by gathering all four 
dictionaries/libraries into a single ``machine object``, as described `here <https://emach.readthedocs.io/en/latest/code.html#machine>`__. This 
section must include a sample code block taking the four user inputs and passing them into a singular ``machine`` object.

Operating Point Inputs from User
*******************************************

The user inputs section of the machine operating point needs to explain to the user what is required as inputs to defining a machine operating point. 
Information required to undetstand all of the inputs defined within the operating point should be included here. This should come in the form of 
an organized table with the following column layout:

1. Keys
2. Descriptions
3. Units (if necessary)

Creating a Machine Operating Point Object
*******************************************

All of the user inputs must be read and constructed into a callable object. This is done by gathering all of the operating point user inputs
into a single ``machine operating point`` object, as described `here <https://emach.readthedocs.io/en/latest/code.html#machine-operating-point>`__. 
This section must include a sample code block taking the operating point inputs and passing them into a singular ``machine_operating_point`` object.