import os
import sys
import copy

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")
sys.path.append(os.path.dirname(__file__))

from mach_eval.analyzers.electromagnetic.bim import bim_transient_2tss_analyzer as bim_tran_2tss
from mach_eval.analyzers.electromagnetic.bim.bim_transient_2tss_config import BIM_Transient_2TSS_Config
from mach_eval import AnalysisStep, ProblemDefinition
from bim_transient_2tss_post_analyzer import BIM_Transient_2TSS_PostAnalyzer

############################ Define EMAnalysisStep ###########################
class BIM_Transient_2TSS_ProblemDefinition(ProblemDefinition):
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):
        if hasattr(state.conditions, 'slip_freq'):
            slip_freq = state.conditions.slip_freq
        else:
            slip_freq = state.design.settings.slip_freq
        if hasattr(state.conditions, 'tha_config'):
            tha_config = state.conditions.tha_config
        else:
            slip_freq = state.design.settings.slip_freq
            tha_config = None

        problem = bim_tran_2tss.BIM_Transient_2TSS_Problem(
            state.design.machine, state.design.settings, slip_freq, tha_config)
        return problem

# initialize em analyzer class with FEA configuration
configuration = BIM_Transient_2TSS_Config(
    no_of_rev_1st_TSS = 0.5,
    no_of_rev_2nd_TSS = 0.5,
    no_of_steps_1st_TSS=24,
    no_of_steps_2nd_TSS=32,

    mesh_size=4, # mm
    mesh_size_rotor=1.8, # mm
    airgap_mesh_radial_div=4,
    airgap_mesh_circum_div=720,
    mesh_air_region_scale=1.05,

    only_table_results=False,
    csv_results=("Torque;Force;FEMCoilFlux;LineCurrent;TerminalVoltage;JouleLoss;TotalDisplacementAngle;"
                  "JouleLoss_IronLoss;IronLoss_IronLoss;HysteresisLoss_IronLoss"),
    del_results_after_calc=False,
    run_folder=os.path.dirname(__file__) + "/run_data/jmag_files/",
    jmag_csv_folder=os.path.dirname(__file__) + "/run_data/jmag_files/jmag_csv/",

    max_nonlinear_iterations=50,
    multiple_cpus=True,
    num_cpus=4,
    jmag_scheduler=False,
    jmag_visible=True,
    non_zero_end_ring_res = False,
    wait_tha_results = True,
    scale_axial_length = True,
)


bim_transient_2tss_analysis = bim_tran_2tss.BIM_Transient_2TSS_Analyzer(configuration)

# class BIM_Transient_2TSS_PostAnalyzer:
#     def get_next_state(results, in_state):
#         state_out = copy.deepcopy(in_state)
#         machine = state_out.design.machine
#         return state_out

transient_2tss_step = AnalysisStep(BIM_Transient_2TSS_ProblemDefinition, bim_transient_2tss_analysis, BIM_Transient_2TSS_PostAnalyzer)
