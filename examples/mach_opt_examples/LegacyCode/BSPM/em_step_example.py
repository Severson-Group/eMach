import os
import sys

os.chdir(os.path.dirname(__file__))
sys.path.append("../../../..")

from machine_design import BSPMArchitectType1
from specifications.bspm_specification import BSPMMachineSpec

from specifications.machine_specs.bp1_machine_specs import DesignSpec
from specifications.materials.electric_steels import Arnon5
from specifications.materials.jmag_library_magnets import N40H
from specifications.materials.miscellaneous_materials import (
    CarbonFiber,
    Steel,
    Copper,
    Hub,
    Air,
)
from settings.bspm_settings_handler import BSPM_Settings_Handler
from local_analyzers.em import BSPM_EM_Analysis
from specifications.analyzer_config.em_fea_config import JMAG_FEA_Configuration

from problems.bspm_em_problem import BSPM_EM_Problem
from post_analyzers.bpsm_em_post_analyzer import BSPM_EM_PostAnalyzer
from length_scale_step import LengthScaleStep
from mach_eval import AnalysisStep, State, MachineDesigner, Conditions


##############################################################################
############################ Define Design ###################################
##############################################################################

# create specification object for the BSPM machine
machine_spec = BSPMMachineSpec(
    design_spec=DesignSpec,
    rotor_core=Arnon5,
    stator_core=Arnon5,
    magnet=N40H,
    conductor=Copper,
    shaft=Steel,
    air=Air,
    sleeve=CarbonFiber,
    hub=Hub,
)

# initialize BSPMArchitect with machine specification
arch = BSPMArchitectType1(machine_spec)
set_handler = BSPM_Settings_Handler()

bspm_designer = MachineDesigner(arch, set_handler)
# create machine variant using architect
free_var = (
    0.00390399,
    0.00964596,
    35.9925,
    0.00358376,
    0.00722451,
    0.0128492,
    0.0143288,
    180.0,
    0.00514122,
    0.00308507,
    0.00363824,
    0.0,
    0.95,
    0,
    0.05,
    2000,
    25,
    80,
)
# set operating point for BSPM machine


design_variant = bspm_designer.create_design(free_var)

##############################################################################
############################ Define EMAnalysisStep ###########################
##############################################################################


class BSPM_EM_ProblemDefinition:
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):
        problem = BSPM_EM_Problem(state.design.machine, state.design.settings)
        return problem


# initialize em analyzer class with FEA configuration
em_analysis = BSPM_EM_Analysis(JMAG_FEA_Configuration)

em_step = AnalysisStep(BSPM_EM_ProblemDefinition, em_analysis, BSPM_EM_PostAnalyzer)

conditions = Conditions()
state = State(design_variant, conditions)

results1, state_out1 = em_step.step(state)

results2, state_out2 = LengthScaleStep.step(state_out1)
