import os
import sys
import copy

from mach_eval import AnalysisStep, ProblemDefinition
from mach_eval.analyzers.mechanical.SynR import AM_SynR_struct_analyzer as AM_SynR_struct
from mach_eval.analyzers.mechanical.SynR.AM_SynR_struct_config import AM_SynR_Struct_Config
from examples.mach_eval_examples.SynR_eval.AM_SynR_struct_post_analyzer import AM_SynR_Struct_PostAnalyzer

############################ Define Structural Step ###########################
class AM_SynR_Struct_ProblemDefinition(ProblemDefinition):
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):

        problem = AM_SynR_struct.AM_SynR_Struct_Problem(
            state.design.machine, state.design.settings)
        return problem

# initialize em analyzer class with FEA configuration
configuration = AM_SynR_Struct_Config(

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

AM_SynR_struct_analysis = AM_SynR_struct.AM_SynR_Struct_Analyzer(configuration)

structural_AM_step = AnalysisStep(AM_SynR_Struct_ProblemDefinition, AM_SynR_struct_analysis, AM_SynR_Struct_PostAnalyzer)