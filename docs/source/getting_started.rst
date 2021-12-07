Getting Started
===============

This document is designed to serve as an initial introduction to ``MachEval``, a repository for the design, evaluation, and optimization of electric machines. A detailed description of the code docstrings can be found :doc:`here<modules>`. The primary purpose of this document is to highlight the flow of information between various components of the ``MachEval`` repository.

Installation
------------

The current code base can be found `here <https://github.com/Severson-Group/MachEval/>`_, download this branch into a folder in which you wish to run the design optimization. The current version of ``MachEval`` requires Python 3.8 as the ``Protocol`` class for structural sub-typing is utilized. Additional the following dependencies are required:

* numpy
* scipy
* pygmo


Code Overview
-------------

``MachEval`` is a open source code base designed to facilitate with the design, evaluation, and optimization of electrical machines. Since machine design is an extremely broad and varied field, ``MachEval`` is constructed to be as modular and flexible as possible to be able to accommodate as many machine topologies, evaluation processes, and optimization criteria. While certain base machine optimizations are provided in this repository, the code can be easily modified to produce custom optimizations as well.

The ``MachEval`` code base is designed to be used by ``pygmo`` an open source optimization library in python. Documentation for the ``pygmo`` library can be found `here <https://esa.github.io/pygmo2/>`_.

The ``MachEval`` repository contains two sub-modules which interface between ``pygmo`` and one another as shown below. the ``des_opt`` module, short for `Design Optimization` is defined to interface with ``pygmo`` by converting free variables to objective values in the required fitness function. This module is designed to extend the base functionality of ``pygmo`` to handle design optimizations using abstract classes. The ``mach_eval`` module is used to evaluate a machine design produced by ``des_opt``. ``mach-eval`` is an extension of two of the primary abstract classes in the ``des_opt`` module which provide additional structure and framework to handle more complicated design evaluations. The layered structure of ``MachEval`` allows for the higher level modules to be used independently of the lower level packages.


.. figure:: /images/getting_started/CodeOverview.png
   :alt: Trial1 
   :align: center
   :width: 600 


The rest of this document will cover both the ``des_opt`` and ``mach_eval`` modules, explaining their purpose and applications. 

des_opt
-------

.. figure:: /images/getting_started/desopt_Diagram.svg
   :alt: Trial1 
   :align: center
   :width: 400 

The ``des_opt`` module is designed to extend the `user-defined-problem <https://esa.github.io/pygmo2/tutorials/coding_udp_simple.html>`_ definition prescribed by ``pygmo``. In order for ``pygmo`` to run a multi-objective user-defined-problem, the object must have three functions implemented: ``fitness``, ``get_bounds``, and ``get_nobj``. The primary class of the ``des_opt`` module is the ``DesignProblem`` class which implements the required functions. The flow of information between ``pygmo`` and the ``DesignProblem`` can be visualized in the following flowchart. 

.. figure:: /images/RectangleExample/DesOptlFlowChart.svg
   :alt: Trial1 
   :align: center
   :width: 300

The ``DesignProblem`` class is structured such that it takes in several objects on initialization which utilize pythons protocol class introduced in `PEP 544 <https://www.python.org/dev/peps/pep-0544/>`_. These objects and their purpose are summarized as follows:

Designer
	The ``Designer`` protocol converts an input tuple into a ``design`` object.
Evaluator
	The ``Evaluator`` protocol evaluates the ``design`` object for a set of criteria defined in the ``evaluate`` function
DesignSpace
	The ``DesignSpace`` protocol handles converting the results of the evaluation into the objective variables.
DataHandler
	Saves the design, evaluation results, and objective values so that optimization can be paused and resumed.

Additional details of each of these objects can be found in the code documentation. An example optimization of a rectangle using the ``des_opt`` module can be found :doc:`here <rectangle_example>`.

Designer
~~~~~~~~

The ``Designer`` Protocol is used to convert the the free variables from the optimization algorithm, into a ``design`` object. The  ``design`` object, does not have any required function calls, and is used as a container for all the information regarding the design which is being evaluated. In order to be considered a ``Designer`` class the ``create_design`` function must be implemented using the following function signature. 

.. code-block:: python

	@runtime_checkable
	class Designer(Protocol):
		"""Parent class for all designers

		"""
		@abstractmethod
		def create_design(self, x: 'tuple') -> 'Design':
			raise NotImplementedError

Evaluator
~~~~~~~~~

The ``Evaluator`` protocol is used to define an evaluation procedure for the ``design`` object created by the ``Designer``. In order for a class to fulfill the role of an ``Evaluator``, the function call for the ``evaluate`` method must be defined as follows.

.. code-block:: python

	@runtime_checkable
	class Evaluator(Protocol):
		"""Parent class for all design evaluators"""
		@abstractmethod
		def evaluate(self, design: 'Design') -> Any:
			pass

DesignSpace
~~~~~~~~~~~

The ``DesignSpace`` protocol is used to convert the results of the design evaluation back into a form which is usable by the optimization algorithm. Additionally, this is where the other information which the algorithm requires about the design evaluation is injected. The following function signatures must be implemented in order to be considered a ``DesignSpace``.

.. code-block:: python

	class DesignSpace(Protocol):
		"""Parent class for a optimization DesignSpace classes"""
		@abstractmethod
		def check_constraints(self, full_results) -> bool:
			raise NotImplementedError

		@abstractmethod
		def n_obj(self) -> int:
			return NotImplementedError

		@abstractmethod
		def get_objectives(self, valid_constraints, full_results) -> tuple:
			raise NotImplementedError

		@abstractmethod
		def bounds(self) -> tuple:
			raise NotImplementedError


mach-eval
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