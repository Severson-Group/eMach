SynR Structural Analyzer
########################################################################

This analyzer enables the 2D static FEA evaluation of synchronous reluctance (SynR) machine rotors in JMAG.

Model Background
****************

Synchronous reluctance (SynR) machines are electric machines capable of producing electromagnetic torque without the need for a 
rotor-mounted field source. Basic characteristics of the design and analysis of synchronous reluctance machines can be done 
by hand, as is shown in the paper `here <https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5167704>`_. Reluctance rotors
are able to achieve high inductance ratios because of their complex rotor design. This complex rotor design is great for creating
reluctance torque, but can have some unintended consequences regarding mechanical integrity. The following parameter is crucial to
ensuring SynR rotors maintain mechanical integrity under rated conditions:

1) Maximum rotor stress must be below yield stress

* R. R. Moghaddam, F. Magnussen and C. Sadarangani, "A FEM1 investigation on the Synchronous Reluctance Machine rotor geometry with 
  just one flux barrier as a guide toward the optimal barrier's shape," `IEEE EUROCON 2009`, St. Petersburg, Russia, 2009, 
  pp. 663-670, doi: 10.1109/EURCON.2009.5167704.

This analyzer calculates the aforementioned parameter using JMAG's static structural solver.

Input from User
*********************************

To use this analyzer, users must pass in a ``MachineDesign`` object. An instance of the ``MachineDesign`` class can be created by passing in 
``machine`` and ``operating_point`` objects. The machine must be a ``SynR_Machine`` and the ``operating_point`` must be of type 
``SynR_Machine_Oper_Pt``. More information on both these classes is available in the ``SynR Design`` section under ``MACHINE DESIGNS``. To 
initialize the ``SynR_Structural_Analyzer``, users must also specify analyzer configuration parameters.

The tables below provide the input expected by the ``MachineDesign`` class and the configuration input required to initialize the 
``SynR_Structural_Analyzer``.

.. csv-table:: `MachineDesign Input`
   :file: input_SynR_struct_analyzer.csv
   :widths: 70, 70
   :header-rows: 1

.. csv-table:: `SynR_Structural_Analyzer Initialization`
   :file: init_SynR_struct_analyzer.csv
   :widths: 70, 70
   :header-rows: 1

Example code initializing the machine design for the optimized SynR design provided in the example found in the ``SynR Design`` section of 
``MACHINE DESIGNS`` is shown below. An identical file titled ``example_SynR_machine`` is stored in the ``SynR_eval`` folder within the 
``mach_eval_examples`` folder in the ``examples`` folder of ``eMach``.

.. code-block:: python

    import os
    import sys

    from mach_eval.machines.materials.electric_steels import (Arnon5)
    from mach_eval.machines.materials.miscellaneous_materials import (
        Steel,
        Copper,
        Air,
    )
    from mach_eval.machines.SynR.SynR_machine import SynR_Machine
    from mach_eval.machines.SynR.SynR_machine_oper_pt import SynR_Machine_Oper_Pt

    SynR_dimensions = {
        'alpha_b': 135,
        'r_sh': 6,
        'r_ri': 6,
        'r_ro': 49,
        'r_f1': 0.1,
        'r_f2': 0.1,
        'r_f3': 0.1,
        'd_r1': 4,
        'd_r2': 8,
        'd_r3': 8,
        'w_b1': 4,
        'w_b2': 4,
        'w_b3': 4,
        'l_b1': 34.1,
        'l_b2': 24.75,
        'l_b3': 13.1,
        'l_b4': 13,
        'l_b5': 10,
        'l_b6': 7,
        'alpha_st': 25,
        'alpha_so': 12.5,
        'r_si': 50,
        'd_so': 5,
        'd_sp': 9,
        'd_st': 40,
        'd_sy': 36,
        'w_st': 12,
        'l_st': 100,
    }


    SynR_parameters = {
        'p': 2,
        'Q': 12,
        "name": "Example_SynR_Machine",
        'rated_speed': 1800,
        'rated_current': 20,   
    }

    SynR_materials = {
        "air_mat": Air,
        "rotor_iron_mat": Arnon5,
        "stator_iron_mat": Arnon5,
        "coil_mat": Copper,
        "shaft_mat": Steel,
    }

    SynR_winding = {
        "no_of_layers": 2,
        "layer_phases": [ ['U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V'],
                            ['W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U'] ],
        "layer_polarity": [ ['+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-'],
                            ['-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+'] ],
        "pitch": 2,
        "Z_q": 20,
        "Kov": 1.8,
        "Kcu": 0.5,
        "phase_current_offset": 0,
    }

    Example_SynR_Machine = SynR_Machine(
        SynR_dimensions, SynR_parameters, SynR_materials, SynR_winding
    )

    ################ DEFINE SynR operating point ################
    Machine_Op_Pt = SynR_Machine_Oper_Pt(
        speed=1800,
        phi_0 = 0,
        ambient_temp=25,
        rotor_temp_rise=0,
    )

To use this code, another file must be created and placed one level outside of the ``eMach`` folder in the repository in which it lies. The 
objective of this file is to call the example machine (in this case the ``example_SynR_machine.py`` that was just created in the ``SynR_eval``
folder) and create a machine design object. 

.. code-block:: python

    import os
    import sys
    from time import time as clock_time

    os.chdir(os.path.dirname(__file__))

    from eMach.mach_eval import (MachineEvaluator, MachineDesign)
    from eMach.examples.mach_eval_examples.SynR_eval.electromagnetic_step import electromagnetic_step
    from eMach.examples.mach_eval_examples.SynR_eval.structural_step import structural_step
    from eMach.examples.mach_eval_examples.SynR_eval.example_SynR_machine import Example_SynR_Machine, Machine_Op_Pt

    ############################ Create Evaluator ########################
    SynR_evaluator = MachineEvaluator(
        [
            electromagnetic_step,
            structural_step
        ]
    )

    design_variant = MachineDesign(Example_SynR_Machine, Machine_Op_Pt)

    results = SynR_evaluator.evaluate(design_variant)

Example code defining the structural step is provided below. This code defines the analyzer problem class (input to the analyzer), 
initializes the analyzer class with an explanation of the required configurations, and calls the post-analyzer class. The 
``SynR_Structural_PostAnalyzer`` class is used to process the structural data and to print the results. A copy of this file lies in 
the ``eMach\examples\mach_eval_examples\SynR_eval`` folder.

.. code-block:: python

    import os
    import sys
    import copy

    from mach_eval import AnalysisStep, ProblemDefinition
    from mach_eval.analyzers.mechanical.SynR import SynR_struct_analyzer as SynR_struct
    from mach_eval.analyzers.mechanical.SynR.SynR_struct_config import SynR_Struct_Config
    from examples.mach_eval_examples.SynR_eval.SynR_struct_post_analyzer import SynR_Struct_PostAnalyzer

    ############################ Define Structural Step ###########################
    class SynR_Struct_ProblemDefinition(ProblemDefinition):
        """Converts a State into a problem"""

        def __init__(self):
            pass

        def get_problem(state):

            problem = SynR_struct.SynR_Struct_Problem(
                state.design.machine, state.design.settings)
            return problem

    # initialize em analyzer class with FEA configuration
    configuration = SynR_Struct_Config(
        no_of_rev = 1,
        no_of_steps = 72,

        mesh_size=3, # mm
        mesh_size_rotor=0.1, # mm
        airgap_mesh_radial_div=4,
        airgap_mesh_circum_div=720,
        mesh_air_region_scale=1.05,

        only_table_results=False,
        csv_results="CsvOutputCalculation",
        del_results_after_calc=False,
        run_folder=os.path.dirname(__file__) + "/run_data/",
        jmag_csv_folder=os.path.dirname(__file__) + "/run_data/jmag_csv/",

        max_nonlinear_iterations=50,
        multiple_cpus=True,
        num_cpus=4,
        jmag_scheduler=False,
        jmag_visible=True,
        scale_axial_length = True,
    )

    SynR_struct_analysis = SynR_struct.SynR_Struct_Analyzer(configuration)

    structural_step = AnalysisStep(SynR_Struct_ProblemDefinition, SynR_struct_analysis, SynR_Struct_PostAnalyzer)

Output to User
**********************************

The ``SynR_Structural_Analyzer`` returns a dictionary holding the results obtained from the static analysis of the machine. The elements 
of this dictionary and their descriptions are provided below:

.. csv-table:: `SynR_Structural_Analyzer Output`
   :file: output_SynR_struct_analyzer.csv
   :widths: 70, 70, 30
   :header-rows: 1

As mentioned, the post analyzer is necessary to extract and compute the analyzer's computations and to interpret the results. The post analyzer 
contains the following code and lies also in the ``eMach\examples\mach_eval_examples\SynR_eval`` folder. The code contained in the post analyzer, 
in this case to find the maximum induced stress, can be seen here:

.. code-block:: python

    import copy

    class SynR_Struct_PostAnalyzer:
        def get_next_state(results, in_state):
            state_out = copy.deepcopy(in_state)

            ############################ Extract required info ###########################
            struct = results["max_stress"]
            s = struct['Maximum Value']
            max_stress = s[0]
            yield_stress = 300 * 1000000

            ############################ Output #################################
            print("\n************************ STRUCTURAL RESULT ************************")
            print("Maximum Stress = ", max_stress/1000000, " MPa",)
            if max_stress > yield_stress:
                print("This exceeds the yield stress of the rotor!")
            else:
                print("This does not exceed the yield stress of the rotor!")
            print("************************************************************\n")
        

            return state_out

All example SynR evaluation scripts, including the one used for this analyzer, can be found in ``eMach\examples\mach_eval_examples\SynR_eval``,
where the post-analyzer script uses FEA results and calculates the maximum induced stress. This analyzer can be run by simply running 
the ``SynR_evaluator`` file in the aforementioned folder. This example should produce the following results:

.. csv-table:: `SynR_Structural_Analyzer Results`
   :file: results_SynR_struct_analyzer.csv
   :widths: 70, 70, 30
   :header-rows: 1