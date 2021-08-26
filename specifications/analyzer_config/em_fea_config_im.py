
import os

FEMM_FEA_Configuration = {
    "TORQUE_CURRENT_RATIO": 0.975,
    "SUSPENSION_CURRENT_RATIO": 0.025,

    "which_filter": "VariableStatorSlotDepth_VariableStatorYokeDepth",
    "End_Ring_Resistance": 0.0,

    "local_sensitivity_analysis": False,
    "local_sensitivity_analysis_number_of_variants": 20,

    "bool_post_processing": False,
    "flag_optimization": False,
    "bool_re_evaluate": False,
    "bool_re_evaluate_wo_csv": False,
    "delete_results_after_calculation": False,

    "designer.Show": True,
    "designer.MultipleCPUs": True,
    "designer.OnlyTableResults": False,
    "designer.Restart": False,
    "designer.JMAG_Scheduler": False,

    "designer.TranRef-StepPerCycle": 40,
    "designer.number_of_steps_1stTSS": 24,
    "designer.number_of_steps_2ndTSS": 32,
    "designer.number_cycles_prolonged": 0,

    "designer.number_cycles_in_3rdTSS": 0,

    "femm.Coarse_Mesh": True,
    "femm.Coarse_Mesh_Level": 2,
    "femm.deg_per_step": "None",
    "femm.use_fraction": False,

    "ignore_rotor_current_density_constraint": False,

    'run_folder'     : os.path.abspath('') + '/run_data/' ,  #storing FEM files path
    'JMAG_csv_folder': os.path.abspath('') + '/run_data/JMAG_csv/',
    }