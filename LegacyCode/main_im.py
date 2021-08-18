
import sys

sys.path.append("..")

from machine_design import IMArchitectType1
from specifications.im_specification import IMMachineSpec
from specifications.machine_specs.im1_machine_specs import DesignSpec


from specifications.materials.electric_steels import Arnon5
from specifications.materials.jmag_library_magnets import N40H
from specifications.materials.miscellaneous_materials import CarbonFiber, Steel, Copper, Hub, Air


from settings.im_settings_handler import IM_Settings_Handler
# from analyzers import structrual_analyzer as sta

from analyzers.em_im_analyzer import IM_EM_Analysis
from specifications.analyzer_config.em_fea_config import JMAG_FEA_Configuration

from problems.bspm_em_problem import BSPM_EM_Problem
from post_analyzers.bpsm_em_post_analyzer import BSPM_EM_PostAnalyzer
from length_scale_step import LengthScaleStep
from mach_eval import AnalysisStep, State, MachineDesigner, MachineEvaluator

##############################################################################
############################ Define Design ###################################
##############################################################################


# create specification object for the BSPM machine
machine_spec = IMMachineSpec(design_spec=DesignSpec, rotor_core=DesignSpec["Steel"],
                               stator_core=DesignSpec["Steel"], rotor_bar=DesignSpec["bar"], conductor=DesignSpec["coil"],
                               shaft=Air, air=Air, hub=Hub)

print("Steel Material", type(DesignSpec["Steel"]))
# initialize BSPMArchitect with machine specification
arch = IMArchitectType1(machine_spec)
set_handler = IM_Settings_Handler()
#
# bspm_designer = MachineDesigner(arch, set_handler)
# # create machine variant using architect
# free_var = (0.00390399, 0.00964596, 35.9925, 0.00358376, 0.00722451, 0.0128492,
#             0.0143288, 180.0, 0.00514122, 0.00308507, 0.00363824, 0.0, 0.95, 0,
#             0.05, 200000, 80)
# # set operating point for BSPM machine
#
# design_variant = bspm_designer.create_design(free_var)
#
# ##############################################################################
# ############################ Define struct AnalysisStep ######################
# ##############################################################################
#
# stress_limits={'rad_sleeve': -100E6,
#                'tan_sleeve': 1300E6,
#                'rad_magnets': 0,
#                'tan_magnets': 80E6}
#
# # spd = sta.SleeveProblemDef(design_variant)
# # problem = spd.get_problem()
# ana = sta.SleeveAnalyzer(stress_limits)
# # sleeve_dim = ana.analyze(problem)
# # print(sleeve_dim)
#
#
# class StructPostAnalyzer:
#     """Converts a State into a problem"""
#     def __init__(self):
#         pass
#
#     def get_next_state(results, in_state):
#         state_out = in_state
#         return state_out
#
#
# struct_step = AnalysisStep(sta.SleeveProblemDef, ana, StructPostAnalyzer)
#
# ##############################################################################
# ############################ Define em AnalysisStep ##########################
# ##############################################################################
#
#
# class BSPM_EM_ProblemDefinition():
#     """Converts a State into a problem"""
#
#     def __init__(self):
#         pass
#
#     def get_problem(state):
#         problem = BSPM_EM_Problem(state.design.machine, state.design.settings)
#         return problem
#
#
# # initialize em analyzer class with FEA configuration
# em_analysis = BSPM_EM_Analysis(JMAG_FEA_Configuration)
#
# # define em step
# em_step = AnalysisStep(BSPM_EM_ProblemDefinition, em_analysis, BSPM_EM_PostAnalyzer)
#
# # evaluate machine design
# evaluator = MachineEvaluator([struct_step, em_step, LengthScaleStep])
# results = evaluator.evaluate(design_variant)
#
