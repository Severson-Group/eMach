BSPM Machine Constants Analyzer
########################################################################

This analyzer determines the machine constants (:math:`K_t, K_f, K_\delta` and :math:`K_\Phi`) of a given BSPM machine design.

Model Background
****************

This analyzer utilizes scripts within eMach to generate `BSPM_Machine` and `BSPM_Machine_Oper_Pt` objects for performing machine constant analysis.



Input from User
*********************************

In order to define the problem class, user must specify the geometry as well as the operating point of the BSPM machine.
For defining the `BSPM_Machine` and `BSPM_Machine_Oper_Pt` objects, user can refer to :doc:`../machines/bspm/index.rst`

.. code-block:: python

    import mach_eval.analyzers.electromagnetic.bspm.machine_constant.bspm_mach_constants as bmc
    import mach_eval.analyzers.electromagnetic.bspm.machine_constant.bspm_mach_constants as bmc
    from mach_eval.machines.materials.electric_steels import Arnon5
    from mach_eval.machines.materials.jmag_library_magnets import N40H
    from mach_eval.machines.materials.miscellaneous_materials import (
        CarbonFiber,
        Steel,
        Copper,
        Hub,
        Air,
    )
    from mach_eval.machines.bspm import BSPM_Machine
    from mach_eval.machines.bspm.bspm_oper_pt import BSPM_Machine_Oper_Pt
    from mach_eval.analyzers.electromagnetic.bspm.jmag_2d_config import JMAG_2D_Config
    import os
    import numpy as np

    #########################################################
    # CREATE BSPM MACHINE OBJECT
    #########################################################

    ################ DEFINE BP4 ################
    bspm_dimensions = {
        "alpha_st": 31.7088,   #[deg]
        "d_so": 2.02334e-3,     #[m]
        "w_st": 5.95805e-3,     #[m]
        "d_st": 18.4967e-3,     #[m]
        "d_sy": 5.81374e-3,     #[m]
        "alpha_m": 180,         #[m]
        "d_m": 3e-3,            #[m]
        "d_mp": 0,              #[m]
        "d_ri": 0.1e-3,         #[m]
        "alpha_so": 15.5,       #[deg] 
        "d_sp": 2.05e-3,        #[m]
        "r_si": 16.9737e-3,     #[m]
        "alpha_ms": 180,        #[deg]
        "d_ms": 0,              #[m]    
        "r_sh": 8.9e-3,         #[m] 
        "l_st": 25e-3,          #[m]
        "d_sl": 1e-3,           #[m]
        "delta_sl": 9.63e-5,    #[m] 
    }

    bspm_parameters = {
        "p": 1,     # number of pole pairs
        "ps": 2,    # number of suspension pole pairs
        "n_m": 1,   # 
        "Q": 6,     # number of slots
        "rated_speed": 16755.16,    #[rad/s] 
        "rated_power": 8e3,         # [W]   
        "rated_voltage": 8e3/18,   # [V_rms] 
        "rated_current": 18,      # [I_rms] 
        "name": "BP4"
    }

    bspm_materials = {
        "air_mat": Air,
        "rotor_iron_mat": Arnon5,
        "stator_iron_mat": Arnon5,
        "magnet_mat": N40H,
        "rotor_sleeve_mat": CarbonFiber,
        "coil_mat": Copper,
        "shaft_mat": Steel,
        "rotor_hub": Hub,
    }

    bspm_winding = {
        "no_of_layers": 2,
        # layer_phases is a list of lists, the number of lists = no_of_layers
        # first list corresponds to coil sides in first layer
        # second list corresponds to coil sides in second layer
        # the index indicates the slot opening corresponding to the coil side
        # string characters are used to represent the phases
        "layer_phases": [["U", "W", "V", "U", "W", "V"], 
                        ["V", "U", "W", "V", "U", "W"]],
        # layer_polarity is a list of lists, the number of lists = no_of_layers
        # first list corresponds to coil side direction in first layer
        # second list corresponds to coil side direction in second layer
        # the index indicates the slot opening corresponding to the coil side
        # + indicates coil side goes into the page, - indicates coil side comes out of page
        "layer_polarity": [["+", "-", "+", "-", "+", "-"], 
                        ["+", "-", "+", "-", "+", "-"]],
        # coil_groups are a unique property of DPNV windings
        # coil group is assigned corresponding to the 1st winding layer
        "coil_groups": ["b", "a", "b", "a", "b", "a"],
        "pitch": 1,
        "Z_q": 45,
        "Kov": 1.8,
        "Kcu": 0.5,
        # add phase current offset to know relative rotor / current angle for creating Iq
        "phase_current_offset": -30  
    }

    bp4 = BSPM_Machine(
        bspm_dimensions, bspm_parameters, bspm_materials, bspm_winding
    )

    #########################################################
    # DEFINE BSPM OPERATING POINT
    #########################################################
    bp4_op_pt = BSPM_Machine_Oper_Pt(
        Id=0,               # I_pu
        Iq=0.95,            # I_pu
        Ix=0,               # I_pu
        Iy=0.05,            # I_pu
        speed=160000,       # RPM
        ambient_temp=25,    # C
        rotor_temp_rise=55, # K
    )

    #########################################################
    # DEFINE BSPM JMAG SETTINGS
    #########################################################
    jmag_config = JMAG_2D_Config(
        no_of_rev_1TS=1,
        no_of_rev_2TS=2,
        no_of_steps_per_rev_1TS=36,
        no_of_steps_per_rev_2TS=360,
        mesh_size=2e-3,
        magnet_mesh_size=1e-3,
        airgap_mesh_radial_div=5,
        airgap_mesh_circum_div=720,
        mesh_air_region_scale=1.15,
        only_table_results=False,
        csv_results=(r"Torque;Force;FEMCoilFlux;LineCurrent;TerminalVoltage;JouleLoss;TotalDisplacementAngle;"
                    "JouleLoss_IronLoss;IronLoss_IronLoss;HysteresisLoss_IronLoss"),
        del_results_after_calc=False,
        run_folder=os.path.abspath("") + "/run_data/",
        jmag_csv_folder=os.path.abspath("") + "/run_data/JMAG_csv/",
        max_nonlinear_iterations=50,
        multiple_cpus=True,
        num_cpus=4,
        jmag_scheduler=False,
        jmag_visible=True,
    )

    #########################################################
    # DEFINE BSPM MACHINE CONSTANTS PROBLEM
    #########################################################
    problem = bmc.BSPMMachineConstantProblem(bp4,bp4_op_pt)

    #########################################################
    # DEFINE BSPM MACHINE CONSTANTS ANALYZER
    #########################################################
    analyzer = bmc.BSPMMachineConstantAnalyzer(jmag_config)


Output to User
**********************************

The attributes of the results class can be summarized in the table below:

.. csv-table::  results of bspm machine constant analyzer
   :file: result_bspm_mach_constants.csv
   :widths: 30, 70, 30
   :header-rows: 1

Use the following code to run the example analysis:

.. code-block:: python

    #########################################################
    # SOLVE BSPM MACHINE CONSTANTS PROBLEM
    #########################################################
    result = analyzer.analyze(problem)
    print(result.Kf)
    print(result.Kt)
    print(result.Kdelta)
    print(result.Kphi)

Running the example case returns the following:

.. code-block:: python


The results indicate that the example BSPM machine design has suspension force constant of xxx [N/A], 
torque constant of xxx [N-m/A_pk], displacement stiffness constant of xxx [N/m] and back-EMF constant of xxx [V_rms/rad/s].

   