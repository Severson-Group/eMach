import sys
from copy import deepcopy

sys.path.append("..")

from machine_design import BSPMArchitectType1

from specifications.bspm_specification import BSPMMachineSpec
from specifications.machine_specs.bp1_machine_specs import DesignSpec
from specifications.materials.electric_steels import Arnon5
from specifications.materials.jmag_library_magnets import N40H
from specifications.materials.miscellaneous_materials import CarbonFiber, Steel, Copper, Hub, Air
from specifications.analyzer_config.em_fea_config import JMAG_FEA_Configuration

from problems.bspm_em_problem import BSPM_EM_Problem
from post_analyzers.bpsm_em_post_analyzer import BSPM_EM_PostAnalyzer
from length_scale_step import LengthScaleStep

from settings.bspmsettingshandler import BSPMSettingsHandler
from analyzers.em import BSPM_EM_Analysis
from analyzers import structrual_analyzer as sta
from analyzers import thermal_analyzer as therm

from bspm_opt import BSPMOptimization
from mach_eval import AnalysisStep, MachineDesigner, MachineEvaluator
from des_opt import DesignProblem, DesignOptimizationMOEAD

from datahandler import DataHandler
##############################################################################
############################ Define Design ###################################
##############################################################################

# create specification object for the BSPM machine
machine_spec = BSPMMachineSpec(design_spec=DesignSpec, rotor_core=Arnon5,
                               stator_core=Arnon5, magnet=N40H, conductor=Copper,
                               shaft=Steel, air=Air, sleeve=CarbonFiber, hub=Hub)

# initialize BSPMArchitect with machine specification
arch = BSPMArchitectType1(machine_spec)
set_handler = BSPMSettingsHandler()

bspm_designer = MachineDesigner(arch, set_handler)
##############################################################################
############################ Define Struct AnalysisStep ######################
##############################################################################
stress_limits = {'rad_sleeve': -100E6,
                 'tan_sleeve': 1300E6,
                 'rad_magnets': 0,
                 'tan_magnets': 80E6}
# spd = sta.SleeveProblemDef(design_variant)
# problem = spd.get_problem()
struct_ana = sta.SleeveAnalyzer(stress_limits)


# sleeve_dim = ana.analyze(problem)
# print(sleeve_dim)


class StructPostAnalyzer:
    """Converts a State into a problem"""

    def get_next_state(results, in_state):
        if results is bool:
            raise AttributeError
        else:
            machine = in_state.design.machine
            new_machine = machine.clone(machine_parameter_dict={'d_sl': results[0]})
        state_out = deepcopy(in_state)
        state_out.design.machine = new_machine
        return state_out


struct_step = AnalysisStep(sta.SleeveProblemDef, struct_ana, StructPostAnalyzer)


##############################################################################
############################ Define EM AnalysisStep ##########################
##############################################################################


class BSPM_EM_ProblemDefinition():
    """Converts a State into a problem"""

    def get_problem(state):
        problem = BSPM_EM_Problem(state.design.machine, state.design.settings)
        return problem


# initialize em analyzer class with FEA configuration
em_analysis = BSPM_EM_Analysis(JMAG_FEA_Configuration)

# define em step
em_step = AnalysisStep(BSPM_EM_ProblemDefinition, em_analysis, BSPM_EM_PostAnalyzer)


##############################################################################
############################ Define Thermal AnalysisStep #####################
##############################################################################


class AirflowPostAnalyzer:
    """Converts a State into a problem"""

    def get_next_state(results, in_state):
        if results['valid'] is False:
            raise AttributeError
        else:
            state_out = deepcopy(in_state)
            state_out.conditions.airflow = results['Required Airflow']
        return state_out


thermal_step = AnalysisStep(therm.AirflowProblemDef, therm.AirflowAnalyzer, AirflowPostAnalyzer)


##############################################################################
############################ Define Windage AnalysisStep #####################
##############################################################################


class WindageLossPostAnalyzer:
    """Converts a State into a problem"""

    def get_next_state(results, in_state):
        state_out = deepcopy(in_state)
        state_out.conditions.windage_loss = results
        machine = state_out.design.machine
        state_out.conditions.efficiency = 100 * machine.mech_power / (machine.mech_power + results +
                                                                      state_out.conditions.em['rotor_iron_loss'] +
                                                                      state_out.conditions.em['stator_iron_loss'] +
                                                                      state_out.conditions.em['magnet_loss'])
        return state_out


windage_step = AnalysisStep(therm.WindageProblemDef, therm.WindageLossAnalyzer, WindageLossPostAnalyzer)

# create evaluator
evaluator = MachineEvaluator([struct_step, em_step, LengthScaleStep, thermal_step, windage_step])

# run optimization
bp2 = [0.00275, 0.01141, 44.51, 5.43e-3, 9.09e-3, 16.94e-3, 13.54e-3, 180.0, 3.41e-3, 0, 3e-3]
bounds = [
    [0.7 * bp2[0], 2 * bp2[0]],  # delta_e  
    [0.8 * bp2[1], 1.2 * bp2[1]],  # r_ro    this will change the tip speed
    [0.3 * bp2[2], 0.85 * bp2[2]],  # alpha_st 
    [0.25 * bp2[3], 4 * bp2[3]],  # d_so     
    [0.6 * bp2[4], 1.3 * bp2[4]],  # w_st     
    [0.6 * bp2[5], 1.2 * bp2[5]],  # d_st    
    [0.7 * bp2[6], 1.4 * bp2[6]],  # d_sy     
    [0.6 * bp2[7], 1 * bp2[7]],  # alpha_m  
    [0.5 * bp2[8], 3 * bp2[8]],  # d_m      
    [0 * bp2[9], 7 * bp2[9]],  # d_mp     
    [0.3 * bp2[10], 1 * bp2[10]],  # d_ri 
]

opt_settings = BSPMOptimization(3, bounds)
design_prob = DesignProblem(bspm_designer, evaluator, opt_settings, DataHandler)
design_opt = DesignOptimizationMOEAD(design_prob)

pop_size = 78
gen_size = 10
ini_pop = design_opt.initial_pop(pop_size)
pop = design_opt.run_optimization(ini_pop, gen_size)
