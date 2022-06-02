import numpy as np
from typing import Any
from copy import deepcopy


class ThermalProblemDefinition:
    """Class converts input state into a problem"""

    def get_problem(self, state: "State") -> "Problem":
        """Returns Problem from Input State"""
        # TODO define problem definition
        g_sy = state.conditions.g_sy  # Volumetric loss in Stator Yoke [W/m^3]
        g_th = state.conditions.g_tooth  # Volumetric loss in Stator Tooth [W/m^3]
        w_st = state.design.machine.w_tooth  # Tooth width [m]
        l_st = state.design.machine.l_st  # Stack length [m]
        l_tooth = (
            state.design.machine.r_sy - state.design.machine.r_si
        )  # Tooth length r_sy-r_si [m]
        alpha_q = state.design.machine.alpha_q  # [rad]
        r_so = state.design.machine.r_so  # outer stator radius [m]
        r_sy = state.design.machine.r_sy  # inner stator yoke radius [m]

        k_ins = state.design.machine.ins_mat[
            "k"
        ]  # thermal insulation conductivity (~1)
        w_ins = state.design.machine.w_ins  # insulation thickness [m] (.5mm)
        k_fe = state.design.machine.core_mat["core_therm_conductivity"]
        h = state.design.settings.h  # convection co-eff W/m^2K
        alpha_slot = (
            state.design.machine.alpha_slot
        )  # span of back of stator slot [rad]
        T_coil_max = state.design.machine.coil_mat["max_temp"]  # Max coil temp [K]

        r_si = state.design.machine.r_si  # inner stator radius
        Q_coil = state.conditions.Q_coil  # ohmic loss per coil
        h_slot = (
            state.design.settings.h_slot
        )  # in slot convection coeff [W/m^2K] set to 0

        problem = ThermalProblem(
            g_sy,
            g_th,
            w_st,
            l_st,
            l_tooth,
            alpha_q,
            r_so,
            r_sy,
            k_ins,
            w_ins,
            k_fe,
            h,
            alpha_slot,
            T_coil_max,
            r_si,
            Q_coil,
            h_slot,
        )
        return problem


class ThermalProblem:
    """problem class utilized by the Analyzer
    
    Attributes:
        TODO
    """

    def __init__(
        self,
        g_sy,
        g_th,
        w_st,
        l_st,
        l_tooth,
        alpha_q,
        r_so,
        r_sy,
        k_ins,
        w_ins,
        k_fe,
        h,
        alpha_slot,
        T_coil_max,
        r_si,
        Q_coil,
        h_slot,
    ):
        """Creates problem class
        
        Args:
            TODO
            
        """
        self.g_sy = g_sy
        self.g_th = g_th
        self.w_st = w_st
        self.l_st = l_st
        self.l_tooth = l_tooth  ####
        self.alpha_q = alpha_q
        self.r_so = r_so  #####
        self.r_sy = r_sy

        self.k_ins = k_ins
        self.w_ins = w_ins
        self.k_fe = k_fe
        self.h = h
        self.alpha_slot = alpha_slot
        self.T_coil_max = T_coil_max
        self.r_si = r_si
        self.Q_coil = Q_coil
        self.h_slot = h_slot


class ThermalAnalyzer:
    """"Class Analyzes the CubiodProblem  for volume and Surface Areas"""

    def analyze(problem):
        """Performs Analysis on a problem

        Args:
            problem (me.Problem): Problem Object

        Returns:
            results (Any): 
                Results of Analysis

        """
        g_sy = problem.g_sy
        g_th = problem.g_th
        w_st = problem.w_st
        l_st = problem.l_st
        l_tooth = problem.l_tooth  ####
        alpha_q = problem.alpha_q
        r_so = problem.r_so  #####
        r_sy = problem.r_sy

        k_ins = problem.k_ins
        w_ins = problem.w_ins
        k_fe = problem.k_fe
        h = problem.h
        alpha_slot = problem.alpha_slot
        T_coil_max = problem.T_coil_max
        h_slot = problem.h_slot
        Q_coil = problem.Q_coil

        # r_vect=np.linspace(r_sy,r_so,100)

        Q_tooth = g_th * w_st * l_st * l_tooth / 2
        Q_sy = g_sy * alpha_q / 2 * (r_so ** 2 - r_sy ** 2) * l_st
        zeta = np.sqrt(2 * k_ins / (w_st * w_ins * k_fe))

        M_th = w_st * l_st / (2 * zeta) * np.tanh(zeta * l_tooth)
        R_sy = 1 / (h * r_so * alpha_q * l_st) + np.log(r_so / r_sy) / (
            k_fe * alpha_q * l_st
        )
        V_sy = l_st * (alpha_q / 2) * (r_so ** 2 - r_sy ** 2)
        M_sy = (
            r_sy ** 2 / (2 * k_fe) * np.log(r_sy / r_so)
            + (r_so ** 2 - r_sy ** 2) / (2 * k_fe)
            + V_sy / (h * r_so * alpha_q * l_st)
        )

        R_coil_st = w_ins * zeta / (k_ins * l_st * np.tanh(zeta * l_tooth))
        R_coil_sy = w_ins / (k_ins * r_sy * alpha_slot * l_st)
        R_coil = (2 / R_coil_st + 1 / R_coil_sy) ** -1
        A_cd = (2 * l_tooth + r_sy * alpha_slot) * l_st
        if h_slot < 0.1:
            T_coil = (
                Q_coil * (R_coil + R_sy)
                + g_sy * M_sy
                + 2 * Q_tooth * R_sy
                - M_th * g_th * R_coil
                + Q_tooth * R_coil
            )
            T_sy = g_sy * M_sy + (Q_coil + 2 * Q_tooth) * R_sy

        else:
            R_cd = 1 / (h_slot * (A_cd))
            # print(R_cd,R_coil,R_coil_sy,R_coil_st)
            T_coil = (
                Q_coil * (R_coil + R_sy)
                + g_sy * M_sy
                + 2 * Q_tooth * R_sy
                - M_th * g_th * R_coil
                + Q_tooth * R_coil
            ) / (1 + R_coil / R_cd)
            T_sy = g_sy * M_sy + (Q_coil + 2 * Q_tooth) * R_sy  # Check this math

        valid = True
        if T_coil > T_coil_max:
            valid = False
        return [T_coil, T_sy, Q_coil, Q_sy, Q_tooth, valid]


class ThermalPostAnalyzer:
    """Converts input state into output state for TemplateAnalyzer"""

    def get_next_state(results: Any, stateIn: "me.State") -> "me.State":
        stateOut = deepcopy(stateIn)
        stateOut.conditions.T_coil = results[0]
        stateOut.conditions.T_sy = results[1]
        stateOut.conditions.Q_coil = results[2]
        stateOut.conditions.Q_yoke = results[3]
        stateOut.conditions.Q_tooth = results[4]

        print("Coil Temp is ", results[0])
        print("Stator Temp is ", results[1])
        return stateOut


problem_def = ThermalProblemDefinition()
analyzer = ThermalAnalyzer()
post_analyzer = ThermalPostAnalyzer()

