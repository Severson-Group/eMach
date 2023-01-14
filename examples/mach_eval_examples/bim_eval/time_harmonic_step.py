import os
import sys
import copy

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")
sys.path.append(os.path.dirname(__file__))

from mach_eval.analyzers.electromagnetic.bim import bim_time_harmonic_analyzer as bim_tha
from mach_eval.analyzers.electromagnetic.bim.bim_time_harmonic_analyzer_config import BIM_Time_Harmonic_Analyzer_Config
from mach_eval import AnalysisStep, ProblemDefinition

############################ Define EMAnalysisStep ###########################
class BIM_Time_Harmonic_ProblemDefinition(ProblemDefinition):
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):
        problem = bim_tha.BIM_Time_Harmonic_Problem(state.design.machine, state.design.settings)
        return problem

# os.path.abspath('')
# initialize em analyzer class with FEA configuration
configuration = BIM_Time_Harmonic_Analyzer_Config(
    run_folder=os.path.dirname(__file__) + '/run_data/femm_files/',
    fraction = 1,
    freq_start = 1,
    freq_end = 5,
    no_of_freqs = 5,
    max_freq_error = 0.255,
    get_results_in_t2tss_analyzer = True,
    id_rotor_iron = 100,
    id_rotor_bars = 101,
    id_stator_slots = 102,
    id_stator_iron = 103,
    automesh = False,
    mesh_size_aluminum = 2 * 6,
    mesh_size_steel = 2 * 6,
    mesh_size_airgap = 2 * 0.75,
    mesh_size_copper = 2 * 10,
    mesh_size_other_regions = 20,
    double_cage = False
)

bim_time_harmonic_analysis = bim_tha.BIM_Time_Harmonic_Analyzer(configuration)

class BIM_Time_Harmonic_PostAnalyzer:
    def get_next_state(results, state_in):
        state_out = copy.deepcopy(state_in)
        # state_out.design.settings.slip_freq = results["slip_freq_breakdown_torque"]
        state_out.conditions.slip_freq = results["slip_freq_breakdown_torque"]
        state_out.conditions.breakdown_torque = results["breakdown_torque"]      
        state_out.conditions.tha_config = results["configuration"]
        return state_out

time_harmonic_step = AnalysisStep(BIM_Time_Harmonic_ProblemDefinition, bim_time_harmonic_analysis, BIM_Time_Harmonic_PostAnalyzer)
