import numpy as np


def process_force_xy_data(force_x: np.array, force_y: np.array):
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
    force_avg_magnitude = sum(force_abs) / len(force_abs)
    # Error magnitude
    force_err_abs = (force_abs - force_avg_magnitude) / force_avg_magnitude
    Em = max(abs(force_err_abs))
    # error angle
    force_err_ang = compute_angle_error(
        np.ones(len(force_ang)) * force_average_angle, np.array(force_ang)
    )
    Ea = max(abs(force_err_ang))

    return f_x, f_y, force_avg_magnitude, Em, Ea


def compute_angle_error(alpha_star, alpha_actual):
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
