import numpy as np

class ProcessForceDataProblem:
    """Problem class for x, y force data processing
    Attributes:
        Fx: numpy array of x axis forces against time or position
        Fx: numpy array of y axis forces against time or position
    """

    def __init__(self, Fx, Fy):
        self.Fx = Fx
        self.Fy = Fy

class ProcessForceDataAnalyzer:
    def analyze(self, problem: ProcessForceDataProblem):
        """Processes x-y force data to extract useful information

        Args:
            problem: object of type ProcessForceDataProblem holding force data
        Returns:
            Fx_avg: Average force along x-axis
            Fy_avg: Average force along y-axis
            F_abs_avg: Net average force
            Em: pu variation in force magnitude
            Ea: Angular variation in force orientation
        """
        Fx = problem.Fx
        Fy = problem.Fy

        # Arrays of force magnitude and angle
        F_abs = np.sqrt(np.array(Fx) ** 2 + np.array(Fy) ** 2)
        F_ang = np.arctan2(Fy, Fx) / np.pi * 180 # [deg]
    
        # Average force and angle
        Fx_avg = sum(Fx) / len(Fx)
        Fy_avg = sum(Fy) / len(Fy)
        F_abs_avg = np.sqrt(Fx_avg ** 2 + Fy_avg ** 2) # sum(F_abs) / len(F_abs)
        F_ang_avg = np.arctan2(Fy_avg, Fx_avg) / np.pi * 180 # [deg]

        # Error magnitude and angle
        Em = max(abs((F_abs - F_abs_avg) / F_abs_avg))
        Ea = max(abs(F_ang - F_ang_avg)) # [deg]

        return Fx_avg, Fy_avg, F_abs_avg, Em, Ea
