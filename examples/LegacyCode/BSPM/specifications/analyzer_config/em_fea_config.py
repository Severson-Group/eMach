import os

JMAG_FEA_Configuration = {
    # FEA Setting
    ##########################
    'TranRef-StepPerCycle': 40,
    'number_of_revolution_1TS': 3,
    'number_of_revolution_2TS': 0.5,
    'number_of_steps_per_rev_1TS': 8,  # Should be TSS actually... Also, number_of_steps_1stTTS is not implemented.
    'number_of_steps_per_rev_2TS': 64,
    # use a multiples of 4! # 8*32 # steps for half period (0.5). That is, we implement two time sections, the 1st
    # section lasts half slip period and the 2nd section lasts half fundamental period.
    'number_cycles_prolonged': 1,  # 150
    'OnlyTableResults': False,
    'MultipleCPUs': True,
    'JMAG_Scheduler': False,
    'max_nonlinear_iterations': 50,
    'Csv_Results': r"Torque;Force;FEMCoilFlux;LineCurrent;TerminalVoltage;JouleLoss;TotalDisplacementAngle;JouleLoss_IronLoss;IronLoss_IronLoss;HysteresisLoss_IronLoss",
    ##########################
    # Mesh settings
    ##########################
    'mesh_size': 4 * 1e-3,  # m
    'mesh_magnet_size': 2 * 1e-3,  # m
    'mesh_radial_division': 7,
    'mesh_circum_division': 720,
    'mesh_air_region_scale': 1.15,

    # Aplication settings
    'designer.Show': False,
    'delete_results_after_calculation': False,

    'run_folder': os.path.abspath('') + '/run_data/',  # storing FEM files path
    'JMAG_csv_folder': os.path.abspath('') + '/run_data/JMAG_csv/',
}
