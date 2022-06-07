# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 15:24:23 2022

@author: Martin Johnson
"""
import numpy as np

class WindageLossProblem:
    """Problem analyzer for windage anlyzer
    Attributes:
        Omega: rotational speed [rad/s]
        
        R_ro: outer rotor radius [m]
        
        stack_length: stack length [m]
        
        R_st: inner stator radius [m]
        
        air_gap: airgap length [m]
        
        u_z: axial air flow speed [m/s]
        
        T_air: Air temperature        
    
    
    """
    
    def __init__(
        self, Omega, R_ro, stack_length, R_st, u_z, T_air=25
    ):
        self.Omega = Omega
        self.R_ro = R_ro
        self.stack_length = stack_length
        self.R_st = R_st
        self.air_gap = R_st-R_ro
        self.u_z=u_z
        self.T_air = T_air


class WindageLossAnalyzer:
    """Windage loss analyzer"""
    def analyze(problem):
        """ Calculates total windage loss in machine.
        
        Args:
            problem: problem class
            
        Returns:
            
            windage_loss_total: Total windage loss on rotor
        
        """
        # Omega, R_ro ,stack_length,R_st,air_gap,m_dot_air, T_air=25):

        # %Air friction loss calculation
        nu_0_Air = 13.3e-6  # ;  %[m^2/s] kinematic viscosity of air at 0
        rho_0_Air = 1.29  # ;     %[kg/m^3] Air density at 0
        Shaft = [
            problem.stack_length,  # 1;         %End position of the sections mm (Absolut)
            problem.R_ro,  # 1;         %Rotor Radius
            1,  # 0;         %Shrouded (1) or free surface (0)
            problem.air_gap,
        ]  # 0];        %Airgap in mm
        # Num_shaft_section = 1
        T_Air = (
            problem.T_air
        )  # 20:(120-20)/((SpeedMax-SpeedMin)/SpeedStep):120         #; % Air temperature []

        nu_Air = nu_0_Air * ((T_Air + 273) / (0 + 273)) ** 1.76
        rho_Air = rho_0_Air * (0 + 273) / (T_Air + 273)
        windage_loss_radial = 0

        # Calculation of the section length ...
        L = Shaft[0]  # in meter
        R = Shaft[1]  # radius of air gap
        delta = Shaft[3]  # length of air gap

        # Reynolds number
        Rey = R ** 2 * (problem.Omega) / nu_Air

        if Shaft[2] == 0:  # free running cylinder
            if Rey <= 170:
                c_W = 8.0 / Rey
            elif Rey > 170 and Rey < 4000:
                c_W = 0.616 * Rey ** (-0.5)
            else:
                c_W = 6.3e-2 * Rey ** (-0.225)
            windage_loss_radial = (
                c_W * np.pi * rho_Air * problem.Omega ** 3 * R ** 5 * (1.0 + L / R)
            )

        else:  # shrouded cylinder by air gap from <Loss measurement of a 30 kW High Speed Permanent Magnet Synchronous Machine with Active Magnetic Bearings>
            Tay = (
                R * (problem.Omega) * (delta / nu_Air) * np.sqrt(delta / R)
            )  # Taylor number
            if Rey <= 170:
                c_W = 8.0 / Rey
            elif Rey > 170 and Tay < 41.3:
                # c_W = 1.8 * Rey**(-1) * delta/R**(-0.25) * (R+delta)**2 / ((R+delta)**2 - R**2) # Ye gu's codes
                c_W = (
                    1.8 * (R / delta) ** (0.25) * (R + delta) ** 2 / (Rey * delta ** 2)
                )  # Ashad over Slack 2019/11/21
            else:
                c_W = 7e-3
            windage_loss_radial = (
                c_W * np.pi * rho_Air * problem.Omega ** 3 * problem.R_ro ** 4 * L
            )

        # end friction loss added - 05192018.yegu
        # the friction coefficients from <Rotor Design of a High-Speed Permanent Magnet Synchronous Machine rating 100,000 rpm at 10 kW>
        Rer = rho_Air * (problem.R_ro) ** 2 * problem.Omega / nu_Air
        if Rer <= 30:
            c_f = 64 / (3 * Rer)
        elif Rer > 30 and Rer < 3 * 10 ** 5:
            c_f = 3.87 * Rer ** (-0.5)
        else:
            c_f = 0.146 * Rer ** (-0.2)

        windage_loss_endFace = (
            0.5 * c_f * rho_Air * problem.Omega ** 3 * (problem.R_ro) ** 5
        )

        # Axial air flow of 0.001 kg/sec for cooling based on B. Riemer, M. Leßmann and K. Hameyer, "Rotor design of a high-speed Permanent Magnet Synchronous Machine rating 100,000 rpm at 10kW," 2010 IEEE Energy Conversion Congress and Exposition, Atlanta, GA, 2010, pp. 3978-3985.
        #Q_flow = problem.m_dot_air / rho_Air
        #A_delta = np.pi * (problem.R_st ** 2 - problem.R_ro ** 2)
        vm = problem.u_z
        um = 0.48 * problem.Omega * problem.R_ro
        windage_loss_axial = (
            (2 / 3)
            * np.pi
            * rho_Air
            * (problem.R_st ** 3 - (problem.R_ro) ** 3)
            * vm
            * um
            * problem.Omega
        )

        windage_loss_total = (
            windage_loss_radial + windage_loss_endFace + windage_loss_axial
        )
        return [windage_loss_radial,windage_loss_endFace,windage_loss_axial]
    