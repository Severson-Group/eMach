import numpy as np
import rotor_structural as rs

class SPM_RotorSpeedLimitProblem:
    """Problem class for SPM_RotorSpeedLimitAnalyzer
    
    Attributes:

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
        mat_dict: dict,
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

        Returns:
            problem (RotorSpeedLimitProblem): RotorSpeedLimitProblem
        """

        # Initial structural problem run at 0 [RPM]
        # Q1. Is it necessary/good practice to make below variable self.X?
        rs_problem = rs.SPM_RotorStructuralProblem(r_sh, d_m, r_ro, d_sl, delta_sl, deltaT, 0, mat_dict)
        
        # Create rotor speed array for evaluation
        N = np.linspace(0, int(N_max),int(N_max)+1)

        # Rotor speed unit conversion [RPM] --> [rad/s]
        omega = np.array(N)*(2*np.pi/60) 

        self.sh = rs_problem.sh
        self.rc = rs_problem.rc
        self.pm = rs_problem.pm
        self.sl = rs_problem.sl
        self.deltaT = deltaT
        self.omega = omega

    def __str__(self) -> str:
        return "testing"

class SPM_RotorSpeedLimitAnalyzer:
    def analyze(
            self, 
            problem: "SPM_RotorSpeedLimitProblem",
            ) -> None:
        pass