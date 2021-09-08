Getting Started
===============

This document will outline the installation of ``macheval``	 and how to get started using it to design, evaluate, and optimize electric machines.

Installation
------------

The current code base can be found `here <https://github.com/Severson-Group/MachEval/tree/develop>`_. Download the ``develop`` branch into a folder in which you wish to run the design optimization.

Code Overview
-------------

The ``macheval`` code base is designed to be used by ``pygmo`` an open source optimization library in python. Full documentation for the ``pygmo`` library can be found `here <https://esa.github.io/pygmo2/>`_.

The ``macheval`` repository contains two sub-modules which interface with one another and ``pygmo`` as shown below. the ``des_opt`` module is defined to interface with ``pygmo`` by converting free variables to objective values in the required fitness function. the ``mach_eval`` module is used to evaluate a machine design produced by ``des_opt``.


.. figure:: /images/getting_started/CodeOverview.png
   :alt: Trial1 
   :align: center
   :width: 600 

The primary purpose of ``macheval`` is to act as a module framework in which machine design, evaluation, and optimization can occur. The ``des_opt`` module is built as an extension of the user-defined-problem objects of ``pygmo`` and the ``mach_eval`` module extends certain protocols defined in the ``des_opt`` module. Each higher level module is designed such that it can function without the use of the lower-level modules so long as function calls are satisfied. 

The rest of this document will cover both the ``des_opt`` and ``mach_eval`` modules, explaining their purpose and applications. A detailed description of the code can be found here TODO ADD THIS LINK.

des_opt
-------

.. figure:: /images/getting_started/desopt_Diagram.png
   :alt: Trial1 
   :align: center
   :width: 400 

The ``des_opt`` module is designed to extend the user-defined-problem definition prescribed by ``pygmo``. In order for ``pygmo`` to run a multi-objective user-defined-problem, the object must have three functions implemented: ``fitness``, ``get_bounds``, and ``get_nobj``. The primary class of the ``des_opt`` module is the ``DesignProblem`` class which implements the required functions.

The ``DesignProblem`` class is structured such that it takes in several objects on initialization which utilize pythons protocol class introduced in `PEP 544 <https://www.python.org/dev/peps/pep-0544/>`_. These objects and their purpose are summarized as follows:

Designer
	Responsible for creating the design from the free variables ``x``.
Evaluator
	Evaluates the design from the designer.
Objectives
	Converts the results of the design evaluation into an objectives tuple for return to ``pygmo``. 
	Handles free variable bounds, constraints, and number of objectives.
DataHandler
	Saves the design, evaluation results, and objective values so that optimization can be paused and resumed.

Additional details of each of these objects can be found in the code documentation. An example optimization of a rectangle using the ``des_opt`` module can be found :doc:`here <rectangle_example>`.

mach_eval
---------

.. figure:: /images/getting_started/MachEval.png
   :alt: Trial1 
   :align: center
   :width: 800 

The ``mach-eval`` module is designed as an extension of the ``Designer`` and ``Evaluator`` protocols from the ``des_opt`` module through the use of the ``MachineDesigner`` and ``MachineEvaluator`` classes respectively. These classes are constructed specifically for the design and evaluation of electric machine, however they can be utilized in the optimization of any complex design problem. An example optimization utilizing the ``mach_eval`` module is provided :doc:`here <toy_example>`.

MachineDesigner
~~~~~~~~~~~~~~~

The ``MachineDesigner`` class is a concrete implementation of the ``Designer`` protocol from the ``des_opt`` module. This class is responsible for converting free variables from and optimization into a ``MachineDesign`` object. The ``MachineDesign`` object has two attributes: a ``machine``, and  ``settings``.  The ``machine`` attribute is an object that holds all the relevant information about the machine, including geometric dimensions, material properties, nameplate values, and winding specifications. The ``settings`` object describes the operating conditions (temperatures, currents/drive settings, operating speed/torques) as well as any other required information to evaluate the design.


.. figure:: /images/getting_started/machineDesignerExample.png
   :alt: Trial1 
   :align: center
   :width: 800 
   
The ``MachineDesigner`` requires two objects to be passed in on initialization: An ``Architect`` and a ``SettingsHandler``. These object are defined as protocols and are responsible for the the creation of the ``machine`` and ``settings`` objects respectively.

MachineEvaluator
~~~~~~~~~~~~~~~~

The ``MachineEvaluator`` class implements the ``Evaluator`` protocol from the ``des_opt`` module. This class extracts evaluation results from the ``MachineDesign`` object created by the ``MachineDesigner``. The evaluation process is split into distinct steps which are described by an ``EvaluationStep`` protocol. These steps take in an input ``state``, which holds the ``MachineDesign`` and any results from the previous evaluations, preform some evaluation on the design, and then add the results to the ``state`` object. 

In order to facilitate the use of generalized machine analysis, a concrete implementation of the ``EvaluationStep`` protocol is provided in the form of the ``AnalysisStep``. This class is designed to handle the conversion of a user defined input ''state'' to the form required for a specific ``Analyzer``. The ``AnalysisStep`` class takes in three protocols on initialization:

ProblemDefinition
	Converts the input ``state`` into a ``problem`` class which can be utilized by the ``Analyzer``
Analyzer
	Performs an analysis on an problem. These are designed to handle specific analysis of complex machine design problems.
PostAnalyzer
	Packages the results of the analysis and the initial state back into the the return state
	
.. figure:: /images/getting_started/AnalysisStepExample.png
   :alt: Trial1 
   :align: center
   :width: 800 