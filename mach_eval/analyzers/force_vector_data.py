import numpy as np


class ProcessForceDataProblem:
    """Problem class for x,y force data processing
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
            f_x: Average force along x-axis
            f_y: Average force along y-axis
            f_tot: Net average force
            Em: pu variation in force magnitude
            Ea: Angular variation in force orientation
        """
        force_x = problem.Fx
        force_y = problem.Fy
        # force magnitude and angle
        force_ang = []
        temp_force_ang = np.arctan2(force_y, force_x) / np.pi * 180  # [deg]
        for angle in temp_force_ang:
            force_ang.append(angle)
        force_abs = np.sqrt(np.array(force_x) ** 2 + np.array(force_y) ** 2)
        # average force
        force_average_angle = sum(force_ang) / len(force_ang)
        f_x = sum(force_x) / len(force_x)
        f_y = sum(force_y) / len(force_y)
        f_tot = sum(force_abs) / len(force_abs)
        # Error magnitude
        force_err_abs = (force_abs - f_tot) / f_tot
        Em = max(abs(force_err_abs))
        # error angle
        force_err_ang = self.compute_angle_error(
            np.ones(len(force_ang)) * force_average_angle, np.array(force_ang)
        )
        Ea = max(abs(force_err_ang))

        return f_x, f_y, f_tot, Em, Ea

    def compute_angle_error(self, alpha_star, alpha_actual):
        N = alpha_star.shape[0]  # determine number of input angles
        vectors_star = np.zeros((N, 2))
        vectors = np.zeros((N, 2))
        # unit vectors for desired angle
        vectors_star[:, 0] = np.cos(np.deg2rad(alpha_star))
        vectors_star[:, 1] = np.sin(np.deg2rad(alpha_star))
        # unit vectors for actual angle
        vectors[:, 0] = np.cos(np.deg2rad(alpha_actual))
        vectors[:, 1] = np.sin(np.deg2rad(alpha_actual))
        # determine angle between vectors in degrees (note that this is only the angle magnitude):
        # This is just doing the cross product between all corresponding unit vectors
        error_angle_mag = np.rad2deg(np.arccos((vectors_star * vectors).sum(axis=1)))
        # to determine the error angle direction we can use the cross product between the vectors
        # positive cross product means the desired vector lags the actual vector and the error angle is positive
        sign = np.sign(np.cross(vectors_star, vectors))
        return sign * error_angle_mag
