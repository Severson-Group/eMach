import numpy as np
from matplotlib import pyplot as plt
import rotor_speed_limit as rsl

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
#Setting the machine geometry and operating conditions
######################################################
r_sh = 5E-3 # [m]
d_m = 2E-3 # [m]
r_ro = 12.5E-3 # [m]
deltaT = 0 # [K]
N = 100E3 # [RPM]
d_sl=1E-3 # [m]
delta_sl=-2.4E-5 # [m]

######################################################
#Creating problem and analyzer class
######################################################
problem = rsl.SPM_RotorSpeedLimitProblem(r_sh, d_m, r_ro, d_sl, delta_sl, deltaT, N, mat_dict)

print(problem)
