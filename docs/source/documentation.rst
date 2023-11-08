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