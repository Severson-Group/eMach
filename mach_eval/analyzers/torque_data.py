class ProcessTorqueDataProblem:
    """Problem class for torque data processing
    Attributes:
        torque: numpy array of torque against time or position
    """

    def __init__(self, torque):
        self.torque = torque


class ProcessTorqueDataAnalyzer:
    def analyze(problem: ProcessTorqueDataProblem):
        """Calcuates average torque and torque ripple

        Args:
            problem: object of type ProcessTorqueDataProblem holding torque data
        Returns:
            avg_torque: Average torque calculated from provided data
            torque_ripple: Torque ripple calculated from provided data
        """
        torque = problem.torque
        avg_torque = torque.mean()
        torque_error = torque - avg_torque
        ss_max_torque_error = max(torque_error), min(torque_error)
        torque_ripple = (
            abs(ss_max_torque_error[0] - ss_max_torque_error[1]) / avg_torque
        )
        return avg_torque, torque_ripple
