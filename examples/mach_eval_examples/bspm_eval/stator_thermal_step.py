import os
import sys
from copy import deepcopy
import numpy as np

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"../../..")

from mach_eval.analyzers.mechanical import thermal_stator as st_therm
from mach_eval import AnalysisStep, ProblemDefinition
from mach_opt import InvalidDesign


###################### Define Stator Thermal AnalysisStep #####################
class MyThermalProblemDefinition(ProblemDefinition):
    """Class converts input state into a problem"""

    def get_problem(state):
        """Returns Problem from Input State"""
        # TODO define problem definition
        g_sy = state.conditions.g_sy  # Volumetric loss in Stator Yoke [W/m^3]
        g_th = state.conditions.g_th  # Volumetric loss in Stator Tooth [W/m^3]
        w_st = state.design.machine.w_st  # Tooth width [m]
        l_st = state.design.machine.l_st  # Stack length [m]
        r_sy = state.design.machine.r_so - state.design.machine.d_sy
        alpha_q = 2 * np.pi / state.design.machine.Q  # [rad]
        r_so = state.design.machine.r_so  # outer stator radius [m]

        k_ins = 1  # thermal insulation conductivity (~1)
        w_ins = 0.5e-3  # insulation thickness [m] (.5mm)
        k_fe = state.design.machine.stator_iron_mat["core_therm_conductivity"]
        h = 200  # convection co-eff W/m^2K
        alpha_slot = alpha_q - 2 * np.arctan(
            w_st / (2 * r_sy)
        )  # span of back of stator slot [rad]
        T_ref = 20  # temperature of cooling liquid [K]

        r_si = state.design.machine.r_si  # inner stator radius
        Q_coil = state.conditions.Q_coil  # ohmic loss per coil
        h_slot = 0  # in slot convection coeff [W/m^2K] set to 0

        problem = st_therm.StatorThermalProblem(
            g_sy=g_sy,
            g_th=g_th,
            w_tooth=w_st,
            l_st=l_st,
            alpha_q=alpha_q,
            r_si=r_si,
            r_so=r_so,
            r_sy=r_sy,
            k_ins=k_ins,
            w_ins=w_ins,
            k_fe=k_fe,
            h=h,
            alpha_slot=alpha_slot,
            Q_coil=Q_coil,
            h_slot=h_slot,
            T_ref=T_ref,
        )
        return problem


class MyStatorThermalPostAnalyzer:
    """Converts input state into output state for TemplateAnalyzer"""

    def get_next_state(results, stateIn):
        if results["Coil temperature"] > 300 == True:
            raise InvalidDesign("Coil temperature beyond limits")
        else:
            stateOut = deepcopy(stateIn)
            stateOut.conditions.T_coil = results["Coil temperature"]
            stateOut.conditions.T_sy = results["Stator yoke temperature"]

        print("\nCoil temperature = ", results["Coil temperature"], " degC")
        print("Stator yoke temperature = ", results["Stator yoke temperature"], " degC")
        return stateOut


stator_therm_step = AnalysisStep(
    MyThermalProblemDefinition,
    st_therm.StatorThermalAnalyzer(),
    MyStatorThermalPostAnalyzer,
)
