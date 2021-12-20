import sys
import os, shutil
from collections import defaultdict

sys.path.append("..")

sys.path.append("../")

from machine_design import BSPMArchitectType1
from specifications.bspm_specification import BSPMMachineSpec

from specifications.machine_specs.bp1_machine_specs import DesignSpec
from specifications.materials.electric_steels import Arnon5
from specifications.materials.jmag_library_magnets import N40H
from specifications.materials.miscellaneous_materials import CarbonFiber, Steel, Copper, Hub, Air
from settings.bspmsettingshandler import BSPMSettingsHandler
from settings.bspm_settings import BSPM_EMAnalyzer_Settings
from analyzers.em import BSPM_EM_Analysis
from specifications.analyzer_config.em_fea_config import JMAG_FEA_Configuration

from problems.bspm_em_problem import BSPM_EM_Problem
from post_analyzers.bpsm_em_post_analyzer import BSPM_EM_PostAnalyzer
from length_scale_step import LengthScaleStep
from mach_eval import AnalysisStep, State, MachineDesigner, Conditions


print('The iterative execution will delete contents of existing run_data folder.......')
reply = str(input('Do you want to proceed? (y/n): ')).lower().strip()
if reply[0] == 'n':
    print('Run terminated')
    sys.exit()

print('Proceeding with iterative execution with deletion of existing run_data folder')

# create specification object for the BSPM machine
machine_spec = BSPMMachineSpec(design_spec=DesignSpec, rotor_core=Arnon5,
                               stator_core=Arnon5, magnet=N40H, conductor=Copper,
                               shaft=Steel, air=Air, sleeve=CarbonFiber, hub=Hub)

# initialize BSPMArchitect with machine specification
arch = BSPMArchitectType1(machine_spec)

class BSPM_EM_ProblemDefinition():
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):
        problem = BSPM_EM_Problem(state.design.machine, state.design.settings)
        return problem



electrical_steps_per_rev = 360 #specify the resolution needed per electrical revolution
JMAG_FEA_Configuration.update({'number_of_steps_per_rev_2TS':electrical_steps_per_rev})
JMAG_FEA_Configuration.update({'number_of_steps_per_rev_1TS':0})
JMAG_FEA_Configuration.update({'number_of_revolution_1TS':0})
JMAG_FEA_Configuration.update({'number_of_revolution_2TS':1})
JMAG_FEA_Configuration.update({'iterative_execution':True})#adding another field to JMAG_FEA_Configuration

# ensure magnets are non conducting by setting "EddyCurrentCalculation" to 0 in 'em' script

if not JMAG_FEA_Configuration.get('iterative_execution'):
    raise Exception('The run is not configured for iterative execution')

if not JMAG_FEA_Configuration.get('number_of_steps_per_rev_2TS') % 4 == 0:
    raise Exception('The number of Steps selected is not even and divisible by 4')
# division by 4(or evenly spaced electrical angles) is essential for smooth interpolation of lookup tables

# delete the initial run_data folder present
if os.path.isdir(JMAG_FEA_Configuration['run_folder']):
    print('...............Deleting the run_data directory')
    shutil.rmtree(JMAG_FEA_Configuration['run_folder'])

# dictionary to store data from multiple iterations, commented to save memory

#my_dict = defaultdict(lambda: defaultdict(int))

#Define possible combinations of values to be captured in iterations for LookUpTables
Id = [-1, -0.5, 0, 0.5, 1]
Iq = [-1, -0.5, 0, 0.5, 1]
Ix = [-1, -0.5, 0, 0.5, 1]
Iy = [-1, -0.5, 0, 0.5, 1]

attempt_count = 0

for nIx in range(len(Ix)):
    i_x = Ix[nIx]
    for nIy in range(len(Ix)):
        i_y = Iy[nIy]
        for nId in range(len(Id)):
            i_d = Id[nId]
            for nIq in range(len(Iq)):
                i_q = Iq[nIq]

                attempt_count = attempt_count + 1

                ##############################################################################
                ############################ Define Design ###################################
                ##############################################################################

                set_handler = BSPMSettingsHandler()

                # Machine Designer and Machine Design is a class of mach_eval script
                bspm_designer = MachineDesigner(arch, set_handler)

                # create machine variant using architect
                free_var = (0.00390399, 0.00964596, 35.9925, 0.00358376, 0.00722451, 0.0128492,
                            0.0143288, 180.0, 0.00514122, 0.00308507, 0.00363824, i_d, i_q,
                            i_x,i_y, 2000, 25, 80)
                # set operating point for BSPM machine

                JMAG_FEA_Configuration.update({'iteration_attempt': attempt_count})

                design_variant = bspm_designer.create_design(free_var)

                em_analysis = BSPM_EM_Analysis(JMAG_FEA_Configuration)

                em_step = AnalysisStep(BSPM_EM_ProblemDefinition, em_analysis, BSPM_EM_PostAnalyzer)

                state_condition = Conditions()
                state = State(design_variant, state_condition)

                results1, state_out1 = em_step.step(state)

                results2, state_out2 = LengthScaleStep.step(state_out1)

                em_dict = em_analysis.__dict__
                csv_folder = em_dict['configuration']['JMAG_csv_folder']
                studyname = em_dict.get('study_name')
                fea_data = em_analysis.extract_JMAG_results(csv_folder,studyname)

                # code to store information in default dictionary(to be inserted)
                #
                #


#Restore configuration fields
JMAG_FEA_Configuration.pop('iteration_attempt')
JMAG_FEA_Configuration.pop('iterative_execution')

