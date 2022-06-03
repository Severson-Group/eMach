import numpy as np
from typing import Any
from copy import deepcopy



class StatorThermalProblem:
    """Problem class utilized by the stator thermal analyzer
    
    Attributes:
        g_sy: Volumetric Heating of stator yoke [W/m^3]
        
        g_th: Volumetric Heating of stator tooth [W/m^3]
        
        w_st: Width of stator tooth [m]
        
        l_st: Stack length [m]
        
        l_tooth: Length of stator tooth [m]
        
        alpha_q: slot span 2pi/Q [rad]
        
        r_so: Outer stator radius [m]
        
        r_sy: Radius of inner stator yoke [m]
        
        k_ins: Thermal conductivity of insulation paper [W/m-K]
        
        w_ins: Thickness of Insulation paper [m]
        
        k_fe: Thermal conductivty of stator iron [W/m-K]
        
        h: Convection rate on exterior of stator [W/m^2-K]
        
        alpha_slot: Angle of back of slot on stator yoke [rad]
        
        T_coil_max: Maximum coil temperature [K]
        
        r_si: Inner stator radius [m]
        
        Q_coil: Resistive coil losses [W]
        
        h_slot: Inslot convection rate [W/m^2-K]
    """

    def __init__(
        self,
        g_sy: float,
        g_th: float,
        w_st: float,
        l_st: float,
        l_tooth: float,
        alpha_q: float,
        r_so: float,
        r_sy: float,
        k_ins: float,
        w_ins: float,
        k_fe: float,
        h: float,
        alpha_slot: float,
        T_coil_max: float,
        r_si: float,
        Q_coil: float,
        h_slot: float,
    ):
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


class StatorThermalAnalyzer:
    """"Stator Thermal Analyzer calculates coil temperatures"""

    def analyze(problem):
        """calculates coil temperature from problem class.

        Args:
            problem (StatorThermalProblem): Problem Object

        Returns:
            results : 
                [Coil temperature,
                 Stator Yoke temperature,
                 Coil losses,
                 Yoke losses,
                 Tooth losses,
                 valid temperature flag]

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
            T_coil = (
                Q_coil * (R_coil + R_sy)
                + g_sy * M_sy
                + 2 * Q_tooth * R_sy
                - M_th * g_th * R_coil
                + Q_tooth * R_coil
            ) / (1 + R_coil / R_cd)
            T_sy = g_sy * M_sy + (Q_coil + 2 * Q_tooth) * R_sy  

        valid = True
        if T_coil > T_coil_max:
            valid = False
        return [T_coil, T_sy, Q_coil, Q_sy, Q_tooth, valid]



