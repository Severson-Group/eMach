.. _structural_analyzer:

Structural Analyzer
###################


This page describes how the structural performance of a surface-mounted permanent magnet (SPM) rotor is evaluated using the eMach code base. The structural analyzer implemented is a combination of two analyzers. A base structural analyzer calculates the stress induced in the rotor, and a rotor sleeve analyzer calculates the optimum design of a carbon fiber sleeve. A detailed description of the math and physics for this problem can be found in the `this paper <https://ieeexplore.ieee.org/document/9595523>`_.



Model Background
****************

The SPM rotor can be modeled as a series of concentric cylinders as shown in the figure below. In this case the rotor is assumed to have four regions of varying material: a shaft, rotor back iron, magnets, and a sleeve. The sleeve is designed with an undersized fit in order to provide the compressive force on the rotor.

.. figure:: ./images/Structural/RotorConfig.svg
   :alt: Trial1 
   :align: center
   :width: 600 

.. figure:: ./images/Structural/SleeveOrientation.svg
   :alt: Trial1 
   :align: center
   :width: 600 

Base Structural Analyzer
************************
The base structural analyzer is used to calculate the rotor radial and tangential stress. The base structural analyzer takes in the ``StructuralProblem`` containing ``RotorComponent`` as an input and returns a list of stress values as ``Sigma`` objects for each rotor component. In the current implementation, the base structural analyzer is not called by the user but by the ``SleeveAnalyzer``; therefore does not follow the standard ``get_problem`` function signature of receiving a ``state`` object.
The user is recommended to checkout the ``StructuralProblem,`` and its problem definition ``StructuralProblemDef`` in ``structural_analyzer.py``.

Sleeve Analyzer
***************
The rotor sleeve analyzer described here is used to design an optimal rotor sleeve which minimizes the required sleeve thickness in order to reduce cost, windage loss, and thermal issues. The sleeve analyzer expects a ``SleeveProblem`` in its analyze function signature. The ``SleeveProblemDef`` extracts the relevant information from the input state object to create the required problem object. Unlike the base structural analyzer, the sleeve analyzer is directly called by the ``MachineEvaluator`` object during evaluation. The implementation of ``SleeveProblem`` and ``SleeveProblemDef`` can be found in ``structural_analyzer.py``.


How to use the structural analyzer
**********************************
To use the eMach structural analyzer, the user must import the ``structural_analyzer`` module and call the ``SleeveAnalyzer`` class. The ``SleeveAnalyzer`` class needs a dictionary containing radial and tangential stress limits for the sleeve and magnet as an input. An example of using the structural analyzer is shown in the following snippet.

.. code-block:: python

    from analyzers import structrual_analyzer as sta
    stress_limits = {'rad_sleeve': -100E6 # [Pa],
                 'tan_sleeve': 1300E6 # [Pa],
                 'rad_magnets': 0 # [Pa],
                 'tan_magnets': 80E6 # [Pa]} 
    struct_ana = sta.SleeveAnalyzer(stress_limits)




