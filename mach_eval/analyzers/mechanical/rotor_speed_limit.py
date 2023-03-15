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
        adhesive_dict (dict): adhesive dictionary
        mat_yield_dict (dict): material yield strength dictionary
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
        adhesive_dict: dict,
        mat_yield_dict: dict,
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
            adhesive_dict (dict): adhesive dictionary
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
        self.adhesive_dict = adhesive_dict
        self.mat_yield_dict = mat_yield_dict

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

        adhesive_dict = problem.adhesive_dict
        mat_yield_dict = problem.mat_yield_dict

        # Create Speed Array
        N_samples = N_max/N_step
        N = np.linspace(0,N_max,100000, endpoint=True)

        sta_analyzer = sta.SPM_RotorStructuralAnalyzer()

        for speed in N:
            sta_problem = sta.SPM_RotorStructuralProblem(r_sh, d_m, r_ro, d_sl, delta_sl, deltaT, speed, mat_dict)
            sta_analyze = sta_analyzer.analyze(sta_problem)
            print (i)


######################################################
# Creating the required Material Dictionary
######################################################
mat_dict = {
    'core_material_density': 7650,  # kg/m3
    'core_youngs_modulus': 185E9,  # Pa
    'core_poission_ratio': .3,
    'alpha_rc' : 1.2E-5,

    'magnet_material_density'    : 7450, # kg/m3
    'magnet_youngs_modulus'      : 160E9, # Pa
    'magnet_poission_ratio'      :.24,
    'alpha_pm'                   :5E-6,

    'sleeve_material_density'    : 1800, # kg/m3
    'sleeve_youngs_th_direction' : 125E9,  #Pa
    'sleeve_youngs_p_direction'  : 8.8E9,  #Pa
    'sleeve_poission_ratio_p'    :.015,
    'sleeve_poission_ratio_tp'   :.28,
    'alpha_sl_t'                :-4.7E-7,
    'alpha_sl_r'                :0.3E-6,

    'sleeve_max_tan_stress': 1950E6,  # Pa
    'sleeve_max_rad_stress': -100E6,  # Pa

    'shaft_material_density': 7870,  # kg/m3
    'shaft_youngs_modulus': 206E9,  # Pa
    'shaft_poission_ratio': .3,  # []
    'alpha_sh' : 1.2E-5
}

######################################################
# Creating the required Adhesive Dictionary
######################################################
adhesive_dict = {}

######################################################
# Creating the required Material Yield Stength Dictionary
######################################################
mat_yield_dict = {}

######################################################
#Setting the machine geometry and operating conditions
######################################################
r_sh = 5E-3 # [m]
d_m = 2E-3 # [m]
r_ro = 12.5E-3 # [m]
deltaT = 0 # [K]
N_max = 100E3 # [RPM]
N_step = 100
d_sl=1E-3 # [m]
delta_sl=-2.4E-5 # [m]

######################################################
#Creating problem and analyzer class
######################################################
problem = SPM_RotorSpeedLimitProblem(r_sh, d_m, r_ro, d_sl, delta_sl, deltaT, 
                                     N_max, N_step, mat_dict, adhesive_dict, mat_yield_dict)

analyzer = SPM_RotorSpeedLimitAnalyzer()
analyzer.analyze(problem)