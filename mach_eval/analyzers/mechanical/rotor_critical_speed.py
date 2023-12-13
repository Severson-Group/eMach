import numpy as np


class RotorCritcalSpeedProblem:
    """Problem class for RotorCritcalSpeedProblem"""

    def __init__(
            self, 
            r_sh:float,
            L:float,
            beta_fi:float,
            material:dict,
            ) -> 'RotorCritcalSpeedProblem':
        
        """Creates RotorCritcalSpeedProblem object from input

        Args:
            r_sh (float): shaft radius, in unit [mm]
            L (float): shaft length, in unit [mm] 
            beta_fi (float): boundary condition numerical constant
            material (dict): material dictionary

        Notes:

        * `material` dictionary must contain the following key-value pairs

            youngs_modulus (float): Young's Modulus of the shaft material
            density (float): density of the shaft material

        Returns:
            RotorCritcalSpeedProblem: RotorCritcalSpeedProblem
        """
        self.r_sh = r_sh
        self.L = L
        self.beta_fi = beta_fi
        self.material = material
        np.einsum

    @property
    def I_sh(self):
        """Area moment of inertia of shaft"""
        return (1/4)*np.pi*self.r_sh**4
    
    @property
    def A_sh(self):
        """Cross-sectional area of shaft"""
        return np.pi*self.r_sh**2


class RotorCritcalSpeedAnalyzer:
    """Analyzer class for RotorCritcalSpeedProblem"""

    def __init__(
            self,
            problem: RotorCritcalSpeedProblem
            ) -> 'RotorCritcalSpeedAnalyzer':
        """Creates RotorCritcalSpeedAnalyzer object from input

        Args:
            problem (RotorCritcalSpeedProblem): Problem class

        Returns:
            RotorCritcalSpeedAnalyzer: RotorCritcalSpeedAnalyzer
        """

        self.problem = problem
        self.material = problem.material
        

    @property
    def omega_n(self):
        return self.problem.beta_fi**2*np.sqrt(
            self.material['young_modulus']*self.problem.I_sh/
            (self.material['density']*self.problem.A_sh*self.problem.L**4))

    

if __name__ == "__main__":
    test = RotorCritcalSpeedProblem(0,0,'Steel')
    print(test.material)
    print(type(test.material))