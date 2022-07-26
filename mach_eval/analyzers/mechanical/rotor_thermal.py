import numpy as np
import scipy.optimize as op
import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import analyzers.general.thermal_network as tb


class SPM_RotorThermalProblem:
    """ Problem class for rotor thermal analyzer
    
    Attributes:
        mat_dict (dict): Material Dictionary
        r_sh (float): Shaft radius [m]
        d_ri (float): Back iron thickness [m]
        r_ro (float): Outer rotor radius [m]
        d_sl (float): Sleeve Thickness [m]
        r_si (float): Stator Inner radius [m]
        l_st (float): Stack length [m]
        l_hub (float): hub thickness [m]
        T_ref (float): Air Temperature [C]
        u_z (float): Axial air flow speed [m/s]
        losses (dict): Loss dictionary [W]
        omega (float): Rotational Speed [rad/s]     
        
        R_1 (float): Shaft radius [m]
        R_2 (float): Back iron radius [m]
        R_3 (float): Outer rotor Radius [m]
        R_4 (float): Outer sleeve radius [m]
    
    """

    def __init__(
        self,
        mat_dict: dict,
        r_sh: float,
        d_ri: float,
        r_ro: float,
        d_sl: float,
        r_si: float,
        l_st: float,
        l_hub: float,
        T_ref: float,
        u_z: float,
        losses: dict,
        omega: float,
    ):
        self.mat_dict = mat_dict
        self.r_sh = r_sh
        self.d_ri = d_ri
        self.r_ro = r_ro
        self.d_sl = d_sl
        self.r_si = r_si
        self.l_st = l_st
        self.l_hub = l_hub

        self.losses = losses
        self.T_ref = T_ref
        self.u_z = u_z
        self.omega = omega

        self.R_1 = self.r_sh
        self.R_2 = self.R_1 + self.d_ri
        self.R_3 = self.r_ro
        self.R_4 = self.R_3 + self.d_sl


class SPM_RotorThermalAnalyzer:
    """ Analyzer for rotor thermal problem
    
    Attributes:
        base_ana (tb.ThermalNetworkAnalyzer): Thermal Network Analyzer
    
    """

    def __init__(self):
        self.base_ana = tb.ThermalNetworkAnalyzer()

    def analyze(self, problem: SPM_RotorThermalProblem):
        """ Analyzes input problem for temperature distribution
        
        Args:
            problem (SPM_RotorThermalProblem): input problem
        Returns:
            T (List): Temperature distribuiton in rotor
        """

        N_nodes = 33
        Res = self.create_resistance_network(problem)

        ################################################
        #           Load Losses into loss Vector
        ################################################
        Q_dot = np.zeros([33, 1])
        Q_dot[1] = 0  # No shaft losses
        Q_dot[3] = problem.losses["rotor_iron_loss"]
        Q_dot[5] = problem.losses["magnet_loss"]

        # print('Magnet Losses:',Q_dot[5])
        ################################################
        #    Create Reference Temperature Vector
        ################################################

        T_ref = [
            [0, problem.T_ref],
        ]

        base_prob = tb.ThermalNetworkProblem(Res, Q_dot, T_ref, N_nodes)
        T = self.base_ana.analyze(base_prob)
        return T

    def create_resistance_network(self, problem):
        ################################################
        #           Load Material Properties
        ################################################
        shaft_k = problem.mat_dict["shaft_therm_conductivity"]
        rotor_core_k = problem.mat_dict["core_therm_conductivity"]
        pm_k = problem.mat_dict["magnet_therm_conductivity"]
        sleeve_k = problem.mat_dict["sleeve_therm_conductivity"]
        air_k = problem.mat_dict["air_therm_conductivity"]
        air_mu = problem.mat_dict["air_viscosity"]
        air_cp = problem.mat_dict["air_cp"]
        hub_k = problem.mat_dict["rotor_hub_therm_conductivity"]

        ################################################
        #             Load Operating Point
        ################################################
        omega = problem.omega
        ################################################
        #           Create Material Objects
        ################################################

        ##############
        # Shaft
        ##############
        sh_mat = tb.Material(shaft_k)
        ##############
        # Rotor Core
        ##############
        rc_mat = tb.Material(rotor_core_k)
        ##############
        # PM
        ##############
        pm_mat = tb.Material(pm_k)
        ##############
        # Sleeve
        ##############
        sl_mat = tb.Material(sleeve_k)
        ##############
        # Hub
        ##############
        hub_mat = tb.Material(hub_k)
        ##############
        # Air
        ##############
        air_mat = tb.Material(air_k, cp=air_cp, mu=air_mu)

        ################################################
        #           Define Geometric Values
        ################################################

        ##############
        # Radial Direction
        ##############
        R_1 = problem.R_1
        R_2 = problem.R_2
        R_3 = problem.R_3
        R_4 = problem.R_4
        R_st = problem.r_si
        # delta=problem.delta
        R_rc = (R_1 + R_2) / 2
        R_pm = (R_2 + R_3) / 2
        R_sl = (R_3 + R_4) / 2
        # print(R_1,R_rc,R_2,R_pm,R_3,R_sl,R_4)
        ##############
        # Axial Direction
        ##############
        stack_length = problem.l_st
        # print('stack length is:',stack_length)
        hub_length = problem.l_hub
        shaft_out = 0.030 + hub_length + stack_length
        L_1 = stack_length / 2
        L_2 = stack_length / 2 + hub_length / 2
        L_3 = stack_length / 2 + hub_length
        L_4 = shaft_out
        u_z = problem.u_z

        ################################################
        #           Create Resistance Objects
        ################################################
        Resistances = []
        ##############
        # Path 0
        ##############
        Descr = "Shaft to rotor core interface (Approximated as Plane Wall)"
        A_sh_1 = stack_length * 2 * np.pi * R_1
        Resistances.append(tb.plane_wall(sh_mat, 1, 2, R_1, A_sh_1))
        Resistances[0].Descr = Descr
        ##############
        # Path 1
        ##############
        Descr = "Shaft/RC interface to rotor core center"
        Resistances.append(tb.cylind_wall(rc_mat, 2, 3, R_1, R_rc, stack_length))
        Resistances[1].Descr = Descr
        ##############
        # Path 2
        ##############
        Descr = "Rotor core center to PM/RC interface"
        Resistances.append(tb.cylind_wall(rc_mat, 3, 4, R_rc, R_2, stack_length))
        Resistances[2].Descr = Descr
        ##############
        # Path 3
        ##############
        Descr = "PM/RC interface to PM center"
        Resistances.append(tb.cylind_wall(pm_mat, 4, 5, R_2, R_pm, stack_length))
        Resistances[3].Descr = Descr
        ##############
        # Path 4
        ##############
        Descr = "PM center to PM/sleeve Interface"
        Resistances.append(tb.cylind_wall(pm_mat, 5, 6, R_pm, R_3, stack_length))
        Resistances[4].Descr = Descr
        ##############
        # Path 5
        ##############
        Descr = "PM/Sleeve Interface to sleeve center"
        Resistances.append(tb.cylind_wall(sl_mat, 6, 7, R_3, R_sl, stack_length))
        Resistances[5].Descr = Descr
        ##############
        # Path 6
        ##############
        Descr = "Sleeve center to outer rotor edge"
        Resistances.append(tb.cylind_wall(sl_mat, 7, 8, R_sl, R_4, stack_length))
        Resistances[6].Descr = Descr
        ##############
        # Path 7
        ##############
        Descr = "Outer rotor edge to air"
        A_rotor_out = stack_length * (2 * np.pi * R_4)
        Resistances.append(
            tb.air_gap_conv(air_mat, 8, 0, omega, R_4, R_st, u_z, A_rotor_out)
        )
        print(Resistances[7].h)
        Resistances[7].Descr = Descr
        ##############
        # Path 8
        ##############
        Descr = "Rotor core center to Hub/RotorCore Interface"
        A_rcHub = np.pi * (R_2 ** 2 - R_1 ** 2)
        Resistances.append(tb.plane_wall(rc_mat, 3, 9, L_1, A_rcHub))
        Resistances[8].Descr = Descr
        ##############
        # Path 9
        ##############
        Descr = "PM center to Hub/PM Interface"
        A_pmHub = np.pi * (R_3 ** 2 - R_2 ** 2)
        Resistances.append(tb.plane_wall(pm_mat, 5, 10, L_1, A_pmHub))
        Resistances[9].Descr = Descr
        ##############
        # Path 10
        ##############
        Descr = "Sleeve center to Hub/Sleeve Interface"
        A_slHub = np.pi * (R_4 ** 2 - R_3 ** 2)
        Resistances.append(tb.plane_wall(sl_mat, 7, 11, L_1, A_slHub))
        Resistances[10].Descr = Descr
        ##############
        # Path 11
        ##############
        Descr = "Shaft Center to shaft Inline with Hub center"
        A_sh = np.pi * (R_1 ** 2)
        Resistances.append(tb.plane_wall(sh_mat, 1, 12, L_2, A_sh))
        Resistances[11].Descr = Descr
        ##############
        # Path 12
        ##############
        Descr = "Hub/Rotor Core interface to Center of Hub inline with Rotor Core"
        Resistances.append(tb.plane_wall(hub_mat, 9, 14, L_2 - L_1, A_rcHub))
        Resistances[12].Descr = Descr
        ##############
        # Path 13
        ##############
        Descr = "Hub/PM interface to Center of Hub inline with PM"
        Resistances.append(tb.plane_wall(hub_mat, 10, 15, L_2 - L_1, A_pmHub))
        Resistances[13].Descr = Descr
        ##############
        # Path 14
        ##############
        Descr = "Hub/Sleeve interface to Center of Hub inline with Sleeve"
        Resistances.append(tb.plane_wall(hub_mat, 11, 16, L_2 - L_1, A_slHub))
        Resistances[14].Descr = Descr
        ##############
        # Path 15
        ##############
        Descr = "Shaft inline with Hub center to Hub/Shaft interface"
        A_sh_2 = 2 * np.pi * R_1 * hub_length
        Resistances.append(tb.plane_wall(sh_mat, 12, 13, R_1, A_sh_2))
        Resistances[15].Descr = Descr
        ##############
        # Path 16
        ##############
        Descr = "Hub/Shaft interface to Center of Hub inline with Rotor Core"
        Resistances.append(tb.cylind_wall(hub_mat, 13, 14, R_1, R_rc, hub_length))
        Resistances[16].Descr = Descr
        ##############
        # Path 17
        ##############
        Descr = "Hub inline with Rotor Core to Hub inline with PM"
        Resistances.append(tb.cylind_wall(hub_mat, 14, 15, R_rc, R_pm, hub_length))
        Resistances[17].Descr = Descr
        ##############
        # Path 18
        ##############
        Descr = "Hub inline with PM to Hub inline with Sleeve "
        Resistances.append(tb.cylind_wall(hub_mat, 15, 16, R_pm, R_sl, hub_length))
        Resistances[18].Descr = Descr
        ##############
        # Path 19
        ##############
        Descr = "Shaft inline with Hub center to Shaft Out "
        Resistances.append(tb.plane_wall(sh_mat, 12, 17, L_4 - L_2, A_sh))
        Resistances[19].Descr = Descr
        ##############
        # Path 20
        ##############
        Descr = "Hub inline with Rotor Core to Outer Hub Inline with Rotor Core "
        Resistances.append(tb.plane_wall(hub_mat, 14, 18, L_3 - L_2, A_rcHub))
        Resistances[20].Descr = Descr
        ##############
        # Path 21
        ##############
        Descr = "Hub inline with PM to Outer Hub Inline with PM "
        Resistances.append(tb.plane_wall(hub_mat, 15, 19, L_3 - L_2, A_pmHub))
        Resistances[21].Descr = Descr
        ##############
        # Path 22
        ##############
        Descr = "Hub inline with Sleeve to Outer Hub Inline with Sleeve"
        Resistances.append(tb.plane_wall(hub_mat, 16, 20, L_3 - L_2, A_slHub))
        Resistances[22].Descr = Descr
        ##############
        # Path 23
        ##############
        Descr = "Outer Shaft to Air"
        A_sh_out = (L_4 - L_3) * (np.pi * R_1)
        Resistances.append(tb.shaft_conv(air_mat, 17, 0, omega, R_1, A_sh_out, u_z))
        Resistances[23].Descr = Descr
        ##############
        # Path 24
        ##############
        Descr = "Outer Hub inline with Rotor Core to Air"
        Resistances.append(tb.hub_conv(air_mat, 18, 0, omega, A_rcHub))
        Resistances[24].Descr = Descr
        ##############
        # Path 25
        ##############
        Descr = "Outer Hub inline with PM to Air"
        Resistances.append(tb.hub_conv(air_mat, 19, 0, omega, A_pmHub))
        Resistances[25].Descr = Descr
        ##############
        # Path 26
        ##############
        Descr = "Outer Hub inline with Sleeve to Air"
        Resistances.append(tb.hub_conv(air_mat, 20, 0, omega, A_slHub))
        Resistances[26].Descr = Descr
        ##############
        # Path 27
        ##############
        Descr = "Rotor Core center to Hub/RotorCore Interface"
        A_rcHub = np.pi * (R_2 ** 2 - R_1 ** 2)
        Resistances.append(tb.plane_wall(rc_mat, 3, 21, L_1, A_rcHub))
        Resistances[27].Descr = Descr
        ##############
        # Path 28
        ##############
        Descr = "PM center to Hub/PM Interface"
        A_pmHub = np.pi * (R_3 ** 2 - R_4 ** 2)
        Resistances.append(tb.plane_wall(pm_mat, 5, 22, L_1, A_pmHub))
        Resistances[28].Descr = Descr
        ##############
        # Path 29
        ##############
        Descr = "Sleeve center to Hub/Sleeve Interface"
        A_slHub = np.pi * (R_4 ** 2 - R_3 ** 2)
        Resistances.append(tb.plane_wall(sl_mat, 7, 23, L_1, A_slHub))
        Resistances[29].Descr = Descr
        ##############
        # Path 30
        ##############
        Descr = "Shaft Center to shaft Inline with Hub center"
        A_sh = np.pi * (R_1 ** 2)
        Resistances.append(tb.plane_wall(sh_mat, 1, 24, L_2, A_sh))
        Resistances[30].Descr = Descr
        ##############
        # Path 31
        ##############
        Descr = "Hub/Rotor Core interface to Center of Hub inline with Rotor Core"
        Resistances.append(tb.plane_wall(hub_mat, 21, 26, L_2 - L_1, A_rcHub))
        Resistances[31].Descr = Descr
        ##############
        # Path 32
        ##############
        Descr = "Hub/PM interface to Center of Hub inline with PM"
        Resistances.append(tb.plane_wall(hub_mat, 22, 27, L_2 - L_1, A_pmHub))
        Resistances[32].Descr = Descr
        ##############
        # Path 33
        ##############
        Descr = "Hub/Sleeve interface to Center of Hub inline with Sleeve"
        Resistances.append(tb.plane_wall(hub_mat, 23, 28, L_2 - L_1, A_slHub))
        Resistances[33].Descr = Descr
        ##############
        # Path 34
        ##############
        Descr = "Shaft inline with Hub center to Hub/Shaft interface"
        A_sh_2 = 2 * np.pi * R_1 * hub_length
        Resistances.append(tb.plane_wall(sh_mat, 24, 25, R_1, A_sh_2))
        Resistances[34].Descr = Descr
        ##############
        # Path 35
        ##############
        Descr = "Hub/Shaft interface to Center of Hub inline with Rotor Core"
        Resistances.append(tb.cylind_wall(hub_mat, 25, 26, R_1, R_rc, hub_length))
        Resistances[35].Descr = Descr
        ##############
        # Path 36
        ##############
        Descr = "Hub inline with Rotor Core to Hub inline with PM"
        Resistances.append(tb.cylind_wall(hub_mat, 26, 27, R_rc, R_pm, hub_length))
        Resistances[36].Descr = Descr
        ##############
        # Path 37
        ##############
        Descr = "Hub inline with PM to Hub inline with Sleeve "
        Resistances.append(tb.cylind_wall(hub_mat, 27, 28, R_pm, R_sl, hub_length))
        Resistances[37].Descr = Descr
        ##############
        # Path 38
        ##############
        Descr = "Shaft inline with Hub center to Shaft Out "
        Resistances.append(tb.plane_wall(sh_mat, 24, 29, L_4 - L_2, A_sh))
        Resistances[38].Descr = Descr
        ##############
        # Path 39
        ##############
        Descr = "Hub inline with Rotor Core to Outer Hub Inline with Rotor Core "
        Resistances.append(tb.plane_wall(hub_mat, 26, 30, L_3 - L_2, A_rcHub))
        Resistances[39].Descr = Descr
        ##############
        # Path 40
        ##############
        Descr = "Hub inline with PM to Outer Hub Inline with PM "
        Resistances.append(tb.plane_wall(hub_mat, 27, 31, L_3 - L_2, A_pmHub))
        Resistances[40].Descr = Descr
        ##############
        # Path 41
        ##############
        Descr = "Hub inline with Sleeve to Outer Hub Inline with Sleeve"
        Resistances.append(tb.plane_wall(hub_mat, 28, 32, L_3 - L_2, A_slHub))
        Resistances[41].Descr = Descr
        ##############
        # Path 42
        ##############
        Descr = "Outer Shaft to Air"
        A_sh_out = (L_4 - L_3) * (np.pi * R_1)
        Resistances.append(tb.shaft_conv(air_mat, 29, 0, omega, R_1, A_sh_out, u_z))
        # print(Resistances[42].resistance_value)
        Resistances[42].Descr = Descr
        ##############
        # Path 43
        ##############
        Descr = "Outer Hub inline with Rotor Core to Air"
        Resistances.append(tb.hub_conv(air_mat, 30, 0, omega, A_rcHub))
        Resistances[43].Descr = Descr
        ##############
        # Path 44
        ##############
        Descr = "Outer Hub inline with PM to Air"
        Resistances.append(tb.hub_conv(air_mat, 31, 0, omega, A_pmHub))
        Resistances[44].Descr = Descr
        ##############
        # Path 45
        ##############
        Descr = "Outer Hub inline with Sleeve to Air"
        Resistances.append(tb.hub_conv(air_mat, 32, 0, omega, A_slHub))
        Resistances[45].Descr = Descr

        return Resistances


#%% Airflow Analyzer


class AirflowProblem:
    """Problem class for AirflowAnalyzer
    
    Attributes:
        mat_dict (dict): Material Dictionary
        r_sh (float): Shaft radius [m]
        d_ri (float): Back iron thickness [m]
        r_ro (float): Outer rotor radius [m]
        d_sl (float): Sleeve Thickness [m]
        r_si (float): Stator Inner radius [m]
        l_st (float): Stack length [m]
        l_hub (float): hub thickness [m]
        T_ref (float): Air Temperature [C]
        losses (dict): Loss dictionary [W]
        omega (float): Rotational Speed [rad/s]
        max_temp (float): Max rotor magnet temperature [K]
        therm_prob (Problem): Thermal problem to solve
        therm_ana (Analzyer): Analyzer to solve problem
    """

    def __init__(
        self,
        r_sh: float,
        d_ri: float,
        r_ro: float,
        d_sl: float,
        r_si: float,
        l_st: float,
        l_hub: float,
        T_ref: float,
        losses: dict,
        omega: float,
        max_temp: float,
        mat_dict: dict,
    ):
        self.r_sh = r_sh
        self.d_ri = d_ri
        self.r_ro = r_ro
        self.d_sl = d_sl
        self.r_si = r_si
        self.l_st = l_st
        self.l_hub = l_hub

        self.losses = losses
        self.T_ref = T_ref
        self.omega = omega
        self.max_temp = max_temp
        self.mat_dict = mat_dict
        self.therm_prob = SPM_RotorThermalProblem
        self.therm_ana = SPM_RotorThermalAnalyzer()

    def magnet_temp(self, u_z):
        """Calculate magnet temperature from airflow rate
        
        Args:
            u_z (float): Axial airflow rate [m/s]
            
        Returns:
            T[5] (float): Magnet Temperature
        """

        prob = self.therm_prob(
            self.mat_dict,
            self.r_sh,
            self.d_ri,
            self.r_ro,
            self.d_sl,
            self.r_si,
            self.l_st,
            self.l_hub,
            self.T_ref,
            u_z,
            self.losses,
            self.omega,
        )
        T = self.therm_ana.analyze(prob)
        return T[5]

    def cost(self, u_z):
        """Returns airflow rate as cost function"""
        return u_z


class AirflowAnalyzer:
    """ Analyzer to calculate required airflow in SPM machine"""

    def analyze(self, problem: AirflowProblem):
        """Analyzes input problem to calculate required airflow to cool rotor
        
        Args:
            problem (AirflowProblem): input problem
        Returns:
            results (dict): dictionary with analyzer solution 
        """

        nlc1 = op.NonlinearConstraint(problem.magnet_temp, 0, problem.max_temp)
        const = nlc1
        sol = op.minimize(
            problem.cost, 0, tol=1e-6, constraints=const, bounds=[(0.00001, 1.0)]
        )
        # print(sol.success)
        # print(sol)
        if sol.success == True:
            results = {
                "valid": sol.success,
                "magnet Temp": problem.magnet_temp(sol.x),
                "Required Airflow": sol.x,
            }
            return results
        else:
            results = {
                "valid": sol.success,
                "magnet Temp": problem.magnet_temp(sol.x),
                "Required Airflow": sol.x,
            }

            return results


if __name__ == "__main__":
    # mat_dict=fea_config_dict
    mat_dict = {
        "shaft_therm_conductivity": 51.9,  # W/m-k ,
        "core_therm_conductivity": 28,  # W/m-k
        "magnet_therm_conductivity": 8.95,  # W/m-k ,
        "sleeve_therm_conductivity": 0.71,  # W/m-k,
        "air_therm_conductivity": 0.02624,  # W/m-K
        "air_viscosity": 1.562e-5,  # m^2/s
        "air_cp": 1,  # kJ/kg
        "rotor_hub_therm_conductivity": 205.0,
    }  # W/m-K}

    r_sh = 5e-3  # [m]
    d_m = 3e-3  # [m]
    r_ro = 12.5e-3  # [m]
    d_ri = r_ro - r_sh - d_m  # [m]
    d_sl = 1e-3  # [m]
    l_st = 50e-3  # [m]
    l_hub = 3e-3  # [m]
    T_ref = 25  # [C]
    r_si = r_ro + d_sl + 1e-3  # [m]
    omega = 120e3 * 2 * np.pi / 60  # [rad/s]
    max_temp = 80
    losses = {"rotor_iron_loss": 0.001, "magnet_loss": 135}
    afp = AirflowProblem(
        r_sh,
        d_ri,
        r_ro,
        d_sl,
        r_si,
        l_st,
        l_hub,
        T_ref,
        losses,
        omega,
        max_temp,
        mat_dict,
    )
    ana = AirflowAnalyzer()
    sleeve_dim = ana.analyze(afp)
    print(sleeve_dim)

