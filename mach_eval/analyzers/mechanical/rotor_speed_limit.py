import numpy as np
import rotor_structural as sta

class SPM_RotorSpeedLimitProblem:
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

    def analyze(self, problem: "SPM_RotorSpeedLimitProblem"):
        """Analyze rotor to determine failure material and rotational speed

        Args:
            problem (PM_RotorSpeedLimitProblem): problem for analyzer.

        Returns:
            results (): 
        """
        self.r_sh = problem.r_sh
        self.d_m = problem.d_m
        self.r_ro = problem.r_ro
        self.d_sl = problem.d_sl
        self.delta_sl = problem.delta_sl
        self.deltaT = problem.deltaT
        self.mat_dict = problem.mat_dict

        N_max = problem.N_max
        N_step = problem.N_step
        mat_failure_dict = problem.mat_failure_dict

        # Failure Condition 
        self.mat_fail_cond = np.array([mat_failure_dict["shaft_yield_strength"],
                                      mat_failure_dict["core_yield strength"],
                                      mat_failure_dict["magnet_ultimate_strength"],
                                      mat_failure_dict["sleeve_ultimate_strength"],
                                      mat_failure_dict["adhesive_ultimate_strength"]])
            
        # Vector of radius for materials   
        node = 100
        r_vect_sh=np.linspace(self.r_sh/10000,self.r_sh,node)
        r_vect_rc=np.linspace(self.r_sh,self.r_ro-self.d_m,node)
        r_vect_pm=np.linspace(self.r_ro-self.d_m,self.r_ro,node)
        r_vect_sl=np.linspace(self.r_ro,self.r_ro+self.d_sl,node)
        r_vect_ah = np.array([self.r_ro-self.d_m])
        self.r_vect = np.array([r_vect_sh,r_vect_rc,r_vect_pm,r_vect_sl,r_vect_ah], dtype=object)

        # Create speed Array
        N = np.arange(0,N_max,N_step) 

        for speed in N:            
            # Check if failure is found and determine failure material
            (fail, failure_mat) = self.check_if_fail(speed)      

            # If failure is found, break for loop
            if fail:
                break

        if failure_mat is None:
            # if no failure, return "False"
            return False
        else:
            # if failure is found, return "True", failure material and speed
            return (True, failure_mat, speed)
        
    def check_if_fail(self, speed):
        # Material Array
        # ( Must follow this specific order )
        materials = np.array(["Shaft",
                              "Core",
                              "Magnet",
                              "Sleeve",
                              "Adhesive"])
        
        # Create rotor structral problem
        st_problem = sta.SPM_RotorStructuralProblem(self.r_sh, 
                                                    self.d_m, 
                                                    self.r_ro, 
                                                    self.d_sl, 
                                                    self.delta_sl, 
                                                    self.deltaT, 
                                                    speed, 
                                                    self.mat_dict)

        # Initialize analyzers
        st_analyzer = sta.SPM_RotorStructuralAnalyzer()

        # Analyze rotor structual problem
        st_sigmas = st_analyzer.analyze(st_problem)

        sigma_max = np.zeros(len(materials))
        failure_mat = None

        # Determine maxmium Von Mises Stress for all rotor materials
        for idx,mat in enumerate(materials):
            # Skip the adhesive since it has a special case
            if mat == "Adhesive":
                continue
            
            # Determine tangential and radial stress
            sigma_t = st_sigmas[idx].tangential(self.r_vect[idx])
            sigma_r = st_sigmas[idx].radial(self.r_vect[idx])
            
            # Create static stress problem 
            ss_problem = SteadyStateStressProblem(sigma_t,sigma_r)

            # Analyze static stress problem
            ss_analyzer = SteadyStateStressAnalyzer()
            ss_stress = ss_analyzer.analyze(ss_problem)

            if mat in ["Shaft", "Core"]:
                # Use Von Mises Stress for ductile materials
                sigma_max[idx] = np.max(ss_stress[0])
            else:
                # Use Tresca Stress for brittle material
                sigma_max[idx] = np.max(ss_stress[1])

        # ASSUMED GLUE STRESS TO BE AT MINIMUM OF CORE
        ss_problem = SteadyStateStressProblem(st_sigmas[1].tangential(self.r_ro-self.d_m),
                                         st_sigmas[1].radial(self.r_ro-self.d_m))
        ss_stress = ss_analyzer.analyze(ss_problem)
        sigma_max[-1] = np.min(ss_stress[1])

        # Determine percenatge to failure for all materials
        pct_to_fail = sigma_max/self.mat_fail_cond

        # Check maximum stress against failure condition to determine failure material
        for idx, pct in enumerate(pct_to_fail):
            
            # Failure when pct is @ 100%
            pct_max = 1.0
            if pct >= pct_max:
                failure_mat = materials[idx]
                return (True,failure_mat)
            else:
                pass
            
        return (False, None)
        
class SteadyStateStressProblem:
    def __init__(self,sigma_x,sigma_y,sigma_z = 0) -> "SteadyStateStressProblem":
        """Problem class for SPM_RotorSpeedLimitAnalyzer
    
        Attributes:
            sigma_x (np.array): Tangential Stress Vector [Pa]
            sigma_y (np.array): Radial Stress Vector [Pa]
            sigma_z (float): Axial Stress (Constant) [Pa]

        Returns:
            problem (SteadyStateStressProblem): SteadyStateStressProblem
        """

        self.sigma_x = sigma_x
        self.sigma_y = sigma_y

        # Create np.array with same size as sigma_x and sigma_y, filled with sigma_z value.
        # Default sigma_z value = 0 [Pa]
        self.sigma_z = np.full(len(sigma_x),sigma_z)

        # Stack nominal stress arrays
        self.sigma_normal = np.stack((self.sigma_x, self.sigma_y, self.sigma_z), axis=1)
        
class SteadyStateStressAnalyzer:
    def __init__(self):
        pass

    def analyze(self, problem: "SteadyStateStressProblem"):
        """Analyze method for SPM_RotorSpeedLimitAnalyzer
    
        Attributes:
            problem (SteadyStateStressProblem): SteadyStateStressProblem

        Returns:
            criterial_stress (np.array): [von_mises_stress,tresca_stress]
        """
        
        sigma_normal = problem.sigma_normal

        # Create Mohrs Circle to compute principle stresses
        mohrs_stress = self.create_mohrs_circle(sigma_normal)

        # Compute Von Mises and Tresca Stress
        von_mises_stress = self.compute_von_mises_stress(mohrs_stress)
        tresca_stress = self.compute_tresca_stress(mohrs_stress)

        criterial_stress = np.array([von_mises_stress,tresca_stress])
        return criterial_stress

    def compute_von_mises_stress(self, mohrs_stress):
        """ Determine Von Mises Equivalent Stress.

        Attributes:
            mohrs_stress (np.array): Principle Stresses [sigma_1,sigma_2,sigma_3,tau_max]

        Returns:
            sigma_e (float): Von Mises Equivalent Stress.
        """
        sigma_1 = mohrs_stress[0]
        sigma_2 = mohrs_stress[1]
        sigma_3 = mohrs_stress[2]

        # Compute Von Mises Equivalent Stress 
        sigma_e = np.sqrt(2)/2*np.sqrt((sigma_2-sigma_1)**2+(sigma_3-sigma_1)**2+(sigma_3-sigma_2)**2)
        return sigma_e

    def compute_tresca_stress(self, mohrs_stress):
        """ Determine Tresca Stress (yield) based on MSST/Tresca criterion.

        Attributes:
            mohrs_stress (np.array): Principle Stresses [sigma_1,sigma_2,sigma_3,tau_max]

        Returns:
            sigma_1-sigma_3 (float): Tresca Stress (yield).
        """
        # Compute Tresca/MSST stress (yield)
        sigma_1 = mohrs_stress[0]
        sigma_3 = mohrs_stress[2]
        return sigma_1-sigma_3

    def create_mohrs_circle(self,sigma_normal):
        """ Determine Principle Stresses (sigma_1, sigma_2, sigma_3) 
        and Maximum Shear Stress (tau_maximum) using 3D Mohr's Circle Method.
        ( Applied shear stress terms are omitted in calculation )

        Attributes:
            sigma_normal (np.array): nominal stress arrays
        
        Returns:
            mohrs_result (np.array): numpy array of mohrs cicrle principle stresses and maxmimum shear stress.
        """
    
        # Sort arrays for determining principle stresses
        sigma_normal_s = np.sort(sigma_normal)

        # Split arrays into three arrays
        sigma_principle = [np.array(x) for x in zip(*sigma_normal_s)] 

        # Obtain Principle Stresses
        sigma_1 = sigma_principle[2]
        sigma_2 = sigma_principle[1]
        sigma_3 = sigma_principle[0]

        # Copmute Maximum Shear Stress
        tau_max = (sigma_1-sigma_3)/2

        mohrs_stress = np.array([sigma_1,sigma_2,sigma_3,tau_max])
        return mohrs_stress
        
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
    'adhesive_ultimate_strength': 17.9E6,  # Pa
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
N_step = 100
d_sl=0 # [m]
delta_sl=0 # [m]

######################################################
#Creating problem and analyzer class
######################################################
problem = SPM_RotorSpeedLimitProblem(r_sh, d_m, r_ro, d_sl, delta_sl, deltaT, 
                                     N_max, N_step, mat_dict, mat_failure_dict)

analyzer = SPM_RotorSpeedLimitAnalyzer()
test = analyzer.analyze(problem)
print(test)
