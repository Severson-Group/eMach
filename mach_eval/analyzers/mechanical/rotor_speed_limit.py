import numpy as np
import rotor_structural as sta

class SPM_RotorSpeedLimitProblem:
    """Problem class for SPM_RotorSpeedLimitAnalyzer
    
    Attributes:
        r_sh (float): Shaft outer radius [m].
        d_m (float): Magnet Thickness [m].
        r_ro (float): Outer Rotor Radius [m].
        d_sl (float): Sleeve Thickness [m].
        delta_sl (float): Sleeve Undersize [m].
        deltaT (float): Temperature Rise [K].
        N_max (float): Maximum RPM to evaluate [RPM].
        N_step (float): RPM evaluation step size [RPM].
        mat_dict (dict): material dictionary 
        mat_failure_dict (dict): material yield strength dictionary
    """

    def __init__(
        self,
        r_sh: float,
        d_m: float,
        r_ro: float,
        d_sl: float,
        delta_sl: float,
        deltaT: float,
        N_max: float,
        N_step: float,
        mat_dict: dict,
        mat_failure_dict: dict,
        ) -> "SPM_RotorSpeedLimitProblem":

        """Creates SPM_RotorSpeedLimitAnalyzer object from input

        Args:
            r_sh (float): Shaft outer radius [m].
            d_m (float): Magnet Thickness [m].
            r_ro (float): Outer Rotor Radius [m].
            d_sl (float): Sleeve Thickness [m].
            delta_sl (float): Sleeve Undersize [m].
            deltaT (float): Temperature Rise [K].
            N_max (float): Maximum RPM to evaluate [RPM].
            N_step (float): RPM evaluation step size [RPM].
            mat_dict (dict): material dictionary 
            mat_yield_dict (dict): material yield strength dictionary

        Returns:
            problem (RotorSpeedLimitProblem): RotorSpeedLimitProblem
        """

        self.r_sh = r_sh
        self.d_m = d_m 
        self.r_ro = r_ro
        self.d_sl = d_sl
        self.delta_sl = delta_sl
        self.deltaT = deltaT
        self.N_max = N_max
        self.N_step = N_step
        self.mat_dict = mat_dict
        self.mat_failure_dict = mat_failure_dict


class SPM_RotorSpeedLimitAnalyzer:
    def __init__(self) -> "SPM_RotorSpeedLimitAnalyzer":
        pass

    def analyze(
        self, problem: "SPM_RotorSpeedLimitProblem",
        ) -> None:
        
        """Analyze all rotor speed

        Args:
            problem (PM_RotorSpeedLimitProblem): problem for analyzer.

        Returns:
            results (): Sigma objects
        """
        r_sh = problem.r_sh
        d_m = problem.d_m
        r_ro = problem.r_ro
        d_sl = problem.d_sl
        delta_sl = problem.delta_sl
        deltaT = problem.deltaT
        N_max = problem.N_max
        N_step = problem.N_step
        mat_dict = problem.mat_dict
        mat_failure_dict = problem.mat_failure_dict

        r_vect_sh=np.linspace(r_sh/10000,r_sh,100)
        r_vect_rc=np.linspace(r_sh,r_ro-d_m,100)
        r_vect_pm=np.linspace(r_ro-d_m,r_ro,100)
        r_vect_sl=np.linspace(r_ro,r_ro+d_sl,100)

        # Create Speed Array
        N = np.arange(0,N_max,N_step) 

        sta_analyzer = sta.SPM_RotorStructuralAnalyzer()
        failure_stress_analyzer = static_failure_stress()

        for i in N:
            sta_problem = sta.SPM_RotorStructuralProblem(r_sh, d_m, r_ro, d_sl, delta_sl, deltaT, i, mat_dict)
            sta_sigmas = sta_analyzer.analyze(sta_problem)

            for j in len(r_vect_sh):
                failure_stress_analyzer.von_mises_stress()
                # YOU STOPPED HERE #

            # Check shaft maximum stress
            # if max(sta_sigmas[0].radial(r_vect_sh)) >= mat_failure_dict['core_yield strength']:
            print (i)

class static_failure_stress:
    def __init__(self):
        pass

    def von_mises_stress(self,radial_stress,tangential_stress,shear_stress):
        """ Determine Principle Stresses (sigma_1, sigma_2) 
        and Maximum Shear Stress (tau_maximum) using 2D Mohr's Circle Method
        
        Args:
            radial_stress (float): Radial stress on element (y-dir)
            tangential_stres (float): Tangential stress on element (x-dir)
            shear_stress (float): Shear Stress on element 
            
        Returns:
            mohrs_result (np.array): numpy array of mohrs cicrle principle stresses and maxmimum shear stress
        """

        self.radial_stress = radial_stress
        self.tangential_stress = tangential_stress
        self.shear_stress = shear_stress

        mohrs_result = self.mohrs_circle()
        sigma_1 = mohrs_result[0]
        sigma_2 = mohrs_result[1]

        sigma_e = np.sqrt(sigma_1**2+sigma_2**2-sigma_1*sigma_2)
        print(sigma_e)

        return sigma_e

    def mohrs_circle(self):
        """ Determine Principle Stresses (sigma_1, sigma_2) 
        and Maximum Shear Stress (tau_maximum) using 2D Mohr's Circle Method
        
        Args:
            None

        Returns:
            mohrs_result (np.array): numpy array of mohrs cicrle principle stresses and maxmimum shear stress
        """
        sigma_x = self.tangential_stress
        sigma_y = self.radial_stress
        tau_xy = self.shear_stress

        # Principle Stresses
        sigma_1 = (sigma_x+sigma_y)/2 + np.sqrt(tau_xy**2+((sigma_x-sigma_y)/2)**2)
        sigma_2 = (sigma_x+sigma_y)/2 - np.sqrt(tau_xy**2+((sigma_x-sigma_y)/2)**2)

        # Maximum Shear Stress (magnitude)
        tau_max = np.sqrt(tau_xy**2+((sigma_x-sigma_y)/2)**2)

        mohrs_result = np.array([sigma_1,sigma_2,tau_max])
        return mohrs_result
        

######################################################
# Creating the required Material Dictionary
######################################################
mat_dict = {

    # Material: M19 29-gauge laminated steel
    'core_material_density': 7650,  # kg/m3
    'core_youngs_modulus': 185E9,  # Pa
    'core_poission_ratio': .3,
    'alpha_rc' : 1.2E-5,

    # Material: N40 neodymium magnets
    'magnet_material_density'    : 7450, # kg/m3
    'magnet_youngs_modulus'      : 160E9, # Pa
    'magnet_poission_ratio'      :.24,
    'alpha_pm'                   :5E-6,

    # Material: Carbon Fiber
    'sleeve_material_density'    : 1800, # kg/m3
    'sleeve_youngs_th_direction' : 125E9,  #Pa
    'sleeve_youngs_p_direction'  : 8.8E9,  #Pa
    'sleeve_poission_ratio_p'    :.015,
    'sleeve_poission_ratio_tp'   :.28,
    'alpha_sl_t'                :-4.7E-7,
    'alpha_sl_r'                :0.3E-6,

    'sleeve_max_tan_stress': 1950E6,  # Pa
    'sleeve_max_rad_stress': -100E6,  # Pa

    # Material: 1045 carbon steel
    'shaft_material_density': 7870,  # kg/m3
    'shaft_youngs_modulus': 206E9,  # Pa
    'shaft_poission_ratio': .3,  # []
    'alpha_sh' : 1.2E-5
}

######################################################
# Creating the required Material Yield Stength Dictionary
######################################################
mat_failure_dict = {

    # Material: M19 29-gauge laminated steel
    # Failure Mode: Yield
    'core_yield strength': 359E6,   # Pa

    # Material: N40 neodymium magnets
    # Failure Mode: Ultimate
    'magnet_ultimate_strength': 80E6,   # Pa

    # Material: Carbon Fiber
    # Failure Mode: Ultimate
    'sleeve_ultimate_strength': 1380E6, # Pa

    # Material: 1045 carbon steel
    # Failure Mode: Yield
    'shaft_yield_strength': 405E6,  # Pa

    # Material: LOCTITE® AA 332™
    # Failure Mode: At break (Ultimate)
    'adhesive_ultimate_strength': 1.79E7,  # Pa
}

# Sources
# Steel: https://www.matweb.com/search/DataSheet.aspx?MatGUID=e9c5392fb06542ca95dcce43149106ac
# Magnet: https://www.matweb.com/search/DataSheet.aspx?MatGUID=b9cac0b8154f4718859da1fe3cdc3c90
# Sleeve: https://www.matweb.com/search/datasheet.aspx?matguid=f0231febe90f4b45857f543bb3300f27
# Shaft: https://www.matweb.com/search/DataSheet.aspx?MatGUID=b194a96080b6410ba81734b094a4537c

######################################################
#Setting the machine geometry and operating conditions
######################################################
r_sh = 5E-3 # [m]
d_m = 2E-3 # [m]
r_ro = 12.5E-3 # [m]
deltaT = 0 # [K]
N_max = 100E3 # [RPM]
N_step = 1000
d_sl=1E-3 # [m]
delta_sl=-2.4E-5 # [m]

######################################################
#Creating problem and analyzer class
######################################################
problem = SPM_RotorSpeedLimitProblem(r_sh, d_m, r_ro, d_sl, delta_sl, deltaT, 
                                     N_max, N_step, mat_dict, mat_failure_dict)

analyzer = SPM_RotorSpeedLimitAnalyzer()
analyzer.analyze(problem)

stress = static_failure_stress()
stress.von_mises_stress(200E6,100E6,0)