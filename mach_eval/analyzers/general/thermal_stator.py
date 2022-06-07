import numpy as np
from typing import Any
from copy import deepcopy



class StatorThermalProblem:
    """Problem class utilized by the stator thermal analyzer
    
    Attributes:
        g_sy: Volumetric Heating of stator yoke [W/m^3]
        
        g_th: Volumetric Heating of stator tooth [W/m^3]
        
        w_tooth: Width of stator tooth [m]
        
        l_st: Stack length [m]
        
        l_tooth: Length of stator tooth [m]
        
        alpha_q: slot span 2pi/Q [rad]
        
        r_si: Inner stator radius [m]
        
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
        
        T_ref: Refrence temperature
    """

    def __init__(
        self,
        g_sy: float,
        g_th: float,
        w_tooth: float,
        l_st: float,
        alpha_q: float,
        r_si: float,
        r_so: float,
        r_sy: float,
        k_ins: float,
        w_ins: float,
        k_fe: float,
        h: float,
        alpha_slot: float,
        Q_coil: float,
        h_slot: float,
        T_ref:float
    ):
        self.g_sy = g_sy
        self.g_th = g_th
        self.w_tooth = w_tooth
        self.l_st = l_st
        self.l_tooth = r_sy-r_si  ####
        self.alpha_q = alpha_q
        self.r_so = r_so  #####
        self.r_sy = r_sy

        self.k_ins = k_ins
        self.w_ins = w_ins
        self.k_fe = k_fe
        self.h = h
        self.alpha_slot = alpha_slot
        self.Q_coil = Q_coil
        self.h_slot = h_slot
        self.T_ref= T_ref


class StatorThermalAnalyzer:
    """"Stator Thermal Analyzer calculates coil temperatures"""

    def analyze(self,problem):
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
        w_tooth = problem.w_tooth
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
        h_slot = problem.h_slot
        Q_coil = problem.Q_coil

        # r_vect=np.linspace(r_sy,r_so,100)

        Q_tooth = g_th * w_tooth * l_st * l_tooth / 2
        Q_sy = g_sy * alpha_q / 2 * (r_so ** 2 - r_sy ** 2) * l_st
        zeta = np.sqrt(2 * k_ins / (w_tooth * w_ins * k_fe))

        M_th = w_tooth * l_st / (2 * zeta) * np.tanh(zeta * l_tooth)
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

        #Add back in ref temp
        T_coil=T_coil+problem.T_ref
        T_sy=T_sy+problem.T_ref
        
        results = {'Coil temperature': T_coil,
                   'Stator yoke temperature': T_sy}
        return results



