Code Guidelines
-------------------------------------------

Developers of eMach should read this document to understand expectations of code contributed to the eMach codebase. This document outlines the 
code requirements for ``analyzers`` and ``machine_designs``. Understanding of proper Python coding practices are necessary to contribute to each 
section of ``eMach``.

Analyzers
++++++++++++++++++++++++++++++++++++++++++++

Analyzer modules should be located within ``mach_eval/analyzers`` and then placed within the appropriate subdirectory.

An analyzer module may contain multiple analyzers if they are interdependent. Each analyzer must consist of the following classes:

1. One Analyzer class
2. At least one Problem class  
3. One Results class

Analyzer Class
*******************************************

The Analyzer class is where the analysis operation is expected to occur. Aspects to consider:

1. Required functions:
    a. Each analyzer must provide an ``analyze(problem p)`` function that takes exactly one argument, a problem object, and returns the analysis results.
2. Optional initializer
    a. An initializer may be used to configure the analyzer's state in a manner that will be re-used across multiple problems. 
    b. The developer must have a compelling reason for why this information is not instead provided to the problem object.
3. Code comments 
    a. Provide short description of each argument / return value
    b. Specify argument / return value units

Problem Class
*******************************************

The purpose of the problem class is to provide the analyzer class the necessary information to analyze a problem. Aspects to consider:

1. Naming
    a. The problem class name should begin similarly to the analyzer class's name, i.e. ``ReallyGreatProblem`` for ``ReallyGreatAnalyzer``.
2. Code comments on user input
    a. Provide short description of each argument 
    b. Specify argument units
3. Recommended practices
    a. Provide user data through the problem class initalizer 
    b. Multiple problem classes can be defined for use with a single analyzer so that users can provide differing formats or conceptualizations of the necessary information (perhaps even requiring some computation within the problem class itself prior to being used in the analyzer).

Results Class
*******************************************

The Results class is where the returns of the analysis operation are brought together into a single return object. Aspects to consider:

1. Required functions:
    a. The results class must provide a single ``results(problem p)`` function that takes any applicable information of the analyzer(s) as arguments and returns the results as a single output object.
2. Code comments 
    a. Provide short description of each return value
    b. Specify return value units