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
            torque_avg: Average torque calculated from provided data
            torque_ripple: Torque ripple calculated from provided data
        """
        torque = problem.torque
        torque_avg = sum(torque) / len(torque)
        torque_ripple = max(abs(torque - torque_avg)) / torque_avg
        return torque_avg, torque_ripple
