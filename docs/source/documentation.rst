Documentation Guidelines
-------------------------------------------

Developers of eMach should read this document to understand expectations of the documentation files related to any code contributed to the eMach 
codebase. This document outlines the requirements for the documentation sections related to ``analyzers`` and ``machine_designs``.

Analyzer Documentation
++++++++++++++++++++++++++++++++++++++++++++

Each analyzer within the ``eMach`` codebase must be summarized such that someone with a basic understanding of electric machines can understand the
purpose and structure of the analyzer. The documentation files devoted to each analyzer must contain the following sections:

1. Model Background
2. Inputs from User
3. Outputs to User

Model Background
*******************************************

Provide information to explain the motivation, application, and any other knowledge required to understand
where and how the analyzer can be applied. This 
can be in the form of equations, images, descriptions, and references to publications or other analyzers. Any assumptions that are made must be explained.

Input from User
*******************************************

Detail the required inputs to the problem and analyzer classes. This must include a table with the following three columns:

1. Arguments
2. Descriptions
3. Units (if necessary)

A copy-paste example code block must be included after the table that illustrates the necessary includes, creating a problem object, and creating an analyzer object. 

Output to User
*******************************************

Describe the return values of the analyzer's ``analyze`` function. If there are multiple variables returned (i.e., a tuple or object) provide a table specifying the data with the following columns:

1. Name
2. Description
3. Units (if necessary)

A copy-paste example code block must be included that completes the example code block provided in ``Input from User`` by calling the ``analyze()`` function and rendering the return values. 
It is recommended to include post-processing code (such as creating a plot) to further illustrate the use of the output data.

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