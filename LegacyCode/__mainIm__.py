
import sys

sys.path.append("..")

from machine_design import IMArchitectType1
from specifications.im_specification import IMMachineSpec
from specifications.machine_specs.im1_machine_specs import DesignSpec


from specifications.materials.electric_steels import M19Gauge29
from specifications.materials.rotor_bar import Aluminium
from specifications.materials.miscellaneous_materials import CarbonFiber, Steel, Copper, Hub, Air


from settings.IM_settings_handler import IM_Settings_Handler
# from analyzers import structrual_analyzer as sta

from analyzers.electrical_analysis_im.em_im_analyzer import IM_EM_Analysis
from specifications.analyzer_config.em_fea_config_im import FEMM_FEA_Configuration

from problems.im_em_problem import IM_EM_Problem
from post_analyzers.im_em_post_analyzer import IM_EM_PostAnalyzer
from length_scale_step import LengthScaleStep
from mach_eval import AnalysisStep, State, MachineDesigner, MachineEvaluator

##############################################################################
############################ Define Design ###################################
##############################################################################


# create specification object for the BSPM machine
machine_spec = IMMachineSpec(design_spec=DesignSpec, rotor_core=M19Gauge29,
                               stator_core=M19Gauge29, rotor_bar=Aluminium, conductor=DesignSpec["coil"],
                               shaft=Air, air=Air, hub=Hub)

print("Steel Material", type(DesignSpec["Steel"]))
# initialize BSPMArchitect with machine specification
arch = IMArchitectType1(machine_spec)
set_handler = IM_Settings_Handler()
#
im_designer = MachineDesigner(arch, set_handler)
# # create machine variant using architect
free_var = (113.767,77.9400,2.43798,47.74648292756861,8.909627424964462,
            1.1791492735270337,1.6699405702001604,44.897393083841415,1.0010737572184039,
            0.82554834654,34.230484771383125,
            9.623859913139942,10.240361002369372,0.5785684617867006,0.2892842308933503,
            92.5925925)
design_variant = im_designer.create_design(free_var)


##############################################################################
############################ Define em AnalysisStep ##########################
##############################################################################


class IM_EM_ProblemDefinition():
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):
        problem = IM_EM_Problem(state.design.machine, state.design.settings)
        return problem
#
#
# initialize em analyzer class with FEA configuration
em_analysis = IM_EM_Analysis(FEMM_FEA_Configuration)
#
# define em step
em_step = AnalysisStep(IM_EM_ProblemDefinition, em_analysis, IM_EM_PostAnalyzer)
#
# # evaluate machine design
evaluator = MachineEvaluator([em_step])
results = evaluator.evaluate(design_variant)
#
