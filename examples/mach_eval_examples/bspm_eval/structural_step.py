import os
import sys
from copy import deepcopy

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"../../..")

from mach_eval.analyzers.mechanical import rotor_structural as stra
from mach_eval import AnalysisStep, ProblemDefinition
from mach_opt import InvalidDesign


############################ Define Struct AnalysisStep ######################
stress_limits = {
    "rad_sleeve": -100e6,
    "tan_sleeve": 1300e6,
    "rad_magnets": 0,
    "tan_magnets": 80e6,
}
# spd = sta.SleeveProblemDef(design_variant)
# problem = spd.get_problem()
struct_ana = stra.SPM_RotorSleeveAnalyzer(stress_limits)


class MySleeveProblemDef(ProblemDefinition):
    def get_problem(state):
        design = state.design
        material_dict = {}
        for key, value in design.machine.rotor_iron_mat.items():
            material_dict[key] = value
        for key, value in design.machine.magnet_mat.items():
            material_dict[key] = value
        for key, value in design.machine.rotor_sleeve_mat.items():
            material_dict[key] = value
        for key, value in design.machine.shaft_mat.items():
            material_dict[key] = value

        r_sh = design.machine.r_sh
        r_ro = design.machine.r_ro
        d_m = design.machine.d_m
        N = design.settings.speed
        deltaT = design.settings.rotor_temp_rise

        problem = stra.SPM_RotorSleeveProblem(r_sh, d_m, r_ro, deltaT, material_dict, N)
        return problem


class MyStructPostAnalyzer:
    """Converts a State into a problem"""

    def get_next_state(results, in_state):
        if results is False:
            raise InvalidDesign("Suitable sleeve not found")
        else:
            print("\nSuitable sleeve found! Thickness = ", results[0], " m")
            print("\n")
            machine = in_state.design.machine
            new_machine = machine.clone(dimensions_dict={"d_sl": results[0]})
        state_out = deepcopy(in_state)
        state_out.design.machine = new_machine
        return state_out


struct_step = AnalysisStep(MySleeveProblemDef, struct_ana, MyStructPostAnalyzer)
