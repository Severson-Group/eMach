import os
import sys
from copy import deepcopy
import numpy as np

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"../../..")

from mach_eval.analyzers.mechanical import rotor_thermal as therm
from mach_eval import AnalysisStep, ProblemDefinition
from mach_opt import InvalidDesign


###################### Define Rotor Thermal AnalysisStep #####################
class MyAirflowProblemDef(ProblemDefinition):
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
        for key, value in design.machine.air_mat.items():
            material_dict[key] = value
        for key, value in design.machine.rotor_hub.items():
            material_dict[key] = value

        r_sh = design.machine.r_sh
        d_ri = design.machine.d_ri
        r_ro = design.machine.r_ro
        d_sl = design.machine.d_sl
        r_si = design.machine.r_si
        l_st = design.machine.l_st
        l_hub = 3e-3
        T_ref = design.settings.ambient_temp
        omega = design.settings.speed * 2 * np.pi / 60
        losses = state.conditions.em
        rotor_max_temp = material_dict["magnet_max_temperature"]
        prob = therm.AirflowProblem(
            r_sh=r_sh,
            d_ri=d_ri,
            r_ro=r_ro,
            d_sl=d_sl,
            r_si=r_si,
            l_st=l_st,
            l_hub=l_hub,
            T_ref=T_ref,
            losses=losses,
            omega=omega,
            max_temp=rotor_max_temp,
            mat_dict=material_dict,
        )
        return prob


class MyAirflowPostAnalyzer:
    """Converts a State into a problem"""

    def get_next_state(results, in_state):
        if results["valid"] is False:
            raise InvalidDesign("Magnet temperature beyond limits")
        else:
            state_out = deepcopy(in_state)
            state_out.conditions.airflow = results
        print("\nMagnet temperature = ", results["magnet Temp"][0], " degC")
        print("Required airflow = ", results["Required Airflow"][0], " m/s")
        return state_out


rotor_therm_step = AnalysisStep(
    MyAirflowProblemDef, therm.AirflowAnalyzer(), MyAirflowPostAnalyzer
)

