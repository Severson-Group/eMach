.. _structural_analyzer:

Structural Analyzer
###################


This page describes how the structural performance of a surface-mounted permanent magnet (SPM) rotor is evaluated using the eMach code base. The structural analyzer implemented is a combination of two analyzers. A base structural analyzer calculates the stress induced in the rotor, and a rotor sleeve analyzer calculates the optimum design of a carbon fiber sleeve. A detailed description of the math and physics for this problem can be found in `this paper <https://ieeexplore.ieee.org/document/9595523>`_.

Model Background
****************

The SPM rotor can be modeled as a series of concentric cylinders as shown in the figure below. In this case, the rotor is assumed to have four regions of varying material: a shaft, rotor back iron, magnets, and a sleeve. The sleeve is designed with an undersized fit in order to provide the compressive force on the rotor.

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
The user is recommended to checkout the ``StructuralProblem,`` and its problem definition ``StructuralProblemDef`` in ``structural_analyzer.py`` (see `here <https://github.com/Severson-Group/eMach/tree/develop/mach_eval/analyzers>`_).

Sleeve Analyzer
***************
The rotor sleeve analyzer described here is used to design an optimal rotor sleeve which minimizes the required sleeve thickness in order to reduce cost, windage loss, and thermal issues. The sleeve analyzer expects a ``SleeveProblem`` in its analyze function signature. The ``SleeveProblemDef`` extracts the relevant information from the input state object to create the required problem object. Unlike the base structural analyzer, the sleeve analyzer is directly called by the ``MachineEvaluator`` object during evaluation. The implementation of ``SleeveProblem`` and ``SleeveProblemDef`` can be found in ``structural_analyzer.py``.

Inputs for structural analyzer
******************************************
The current implementation of the structural analyzer requires a material dictionary (``mat_dict``), temperature coefficient, and dimensions of the shaft, rotor core, magnet, and sleeve. The following table shows the list of required inputs for the structural analyzer.

.. csv-table:: Inputs for structural analyzer -- ``mat_dict``
   :file: inputs_mat_dict.csv
   :widths: 70, 70, 30
   :header-rows: 1

.. csv-table:: Inputs for structural analyzer -- Dimensions
   :file: inputs_dimensions.csv
   :widths: 70, 70, 30
   :header-rows: 1

.. csv-table:: Inputs for structural analyzer -- ``stress_limits``
   :file: inputs_sleeve_stress.csv
   :widths: 70, 70, 30
   :header-rows: 1


How to use the structural analyzer
**********************************
To use the eMach structural analyzer, the user must import the ``structural_analyzer`` module and call the ''SleeveProblemDef'', ``SleeveProblem``, and ``SleeveAnalyzer`` class. An example of using the structural analyzer is shown in the following snippet.

.. code-block:: python

    from mach_eval.analyzers import structrual_analyzer as sta

    mat_dict = {
        'core_material_density': 7650,  # kg/m3
        'core_youngs_modulus': 185E9,  # Pa
        'core_poission_ratio': .3,
        'alpha_rc' : 1.2E-5,

        'magnet_material_density'    : 7450, # kg/m3
        'magnet_youngs_modulus'      : 160E9, # Pa
        'magnet_poission_ratio'      :.24,
        'alpha_pm'                   :5E-6,

        'sleeve_material_density'    : 1800, # kg/m3
        'sleeve_youngs_th_direction' : 125E9,  #Pa
        'sleeve_youngs_p_direction'  : 8.8E9,  #Pa
        'sleeve_poission_ratio_p'    :.015,
        'sleeve_poission_ratio_tp'   :.28,
        'alpha_sl_t'                :-4.7E-7,
        'alpha_sl_r'                :0.3E-6,

        'sleeve_max_tan_stress': 1950E6,  # Pa
        'sleeve_max_rad_stress': -100E6,  # Pa

        'shaft_material_density': 7870,  # kg/m3
        'shaft_youngs_modulus': 206E9,  # Pa
        'shaft_poission_ratio': .3,  # []
        'alpha_sh' : 1.2E-5
    }



    stress_limits = {'rad_sleeve': -100E6,
                     'tan_sleeve': 1300E6,
                     'rad_magnets': 0,
                     'tan_magnets': 80E6}
    r_sh = 5E-3
    d_m = 3E-3
    r_ro = 12.5E-2
    deltaT = 10
    N = 10E3
    spd = sta.SleeveProblemDef(mat_dict)
    problem = sta.SleeveProblem(r_sh, d_m, r_ro, deltaT, mat_dict, N)
    ana = sta.SleeveAnalyzer(stress_limits)
    sleeve_dim = ana.analyze(problem)
    print(sleeve_dim)


