import numpy as np


def process_torque_data(torque_arr: np.array):
    torque = torque_arr
    avg_torque = torque.mean()
    torque_error = torque - avg_torque
    ss_max_torque_error = max(torque_error), min(torque_error)
    torque_ripple = abs(ss_max_torque_error[0] - ss_max_torque_error[1]) / avg_torque
    return avg_torque, torque_ripple
