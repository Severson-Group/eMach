import sys
import os
import numpy as np
import pandas as pd

from data_handler import MyDataHandler
from data_analyzer import DataAnalyzer

path = os.path.dirname(__file__)
arch_file = path + r'/opti_arch.pkl'  # specify path where saved data will reside
des_file = path + r'/opti_designer.pkl'
dh = MyDataHandler(arch_file, des_file)  # initialize data handler with required file paths

fitness, free_vars = dh.get_pareto_fitness_freevars()
fts = np.asarray(fitness)

eff = []
for i in range(len(fts[:,1])):
    eff.append(fts[i,1][0])
    
fitness_dict = {'SP': fts[:,0],
                'eff': eff,
                'WR': fts[:,2],}
fitness_df = pd.DataFrame.from_dict(fitness_dict)
fitness_df.to_csv('fitness.csv')

da = DataAnalyzer(path)
# # da.plot_fitness_tradeoff(fitness, rated_power, label=['SP [kW/kg]', '$\eta$ [%]', 'WR [1]', 'Power [kW]'],
# #                           axes=[0,3], filename='pd_vs_power')
da.plot_pareto_front(points=fitness, label=['Cost [USD]', '-$\eta$ [%]', 'WR [1]'])

# fitness, free_vars = dh.get_archive_data()
# var_label = [
#               '$\delta_e$ [m]', 
#               r'$\alpha_{st} [deg]$', 
#               '$d_{so}$ [m]',
#               '$w_{st}$ [m]',
#               '$d_{st}$ [m]',
#               '$d_{sy}$ [m]',
#               r'$del_{dsp}$ [m]',
#               '$i_q$ [pu]'
#             ]

# bp2 = (0.002, 60, 5.43e-3, 15.09e-3, 16.94e-3, 6e-3, 0.95)
# # # bounds for pygmo optimization problem
# bounds = [
#     [1 * bp2[0], 2.5 * bp2[0]],     # delta_e
#     [0.4 * bp2[1], 0.9 * bp2[1]],   # alpha_st
#     [0.2 * bp2[2], 3 * bp2[2]],     # d_so
#     [0.1 * bp2[3], 2.5 * bp2[3]],   # w_st
#     [0.2 * bp2[4], 2.5 * bp2[4]],   # d_st
#     [0.2 * bp2[5], 2 * bp2[5]],     # d_sy
#     [0, 1 * bp2[2]],                # del_dsp
#     [1 * bp2[6], 3/0.95 * bp2[6]]   # Iq
# ]
# da.plot_x_with_bounds(free_vars, var_label, bounds)
dh.select_designs()

proj_120_ = dh.get_machine( 'proj_120_')
print("proj_120_ d_st", proj_120_.d_st)
