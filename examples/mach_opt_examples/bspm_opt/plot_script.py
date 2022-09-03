import os
import numpy as np
import pandas as pd

from my_data_handler import MyDataHandler
from my_plotting_functions import DataAnalyzer

path = os.path.dirname(__file__)
arch_file = path + r'/opti_arch.pkl'  # specify path where saved data will reside
des_file = path + r'/opti_designer.pkl'
dh = MyDataHandler(arch_file, des_file)  # initialize data handler with required file paths
da = DataAnalyzer(path)

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

da.plot_pareto_front(points=fitness, label=['SP [kW/kg]', '-$\eta$ [%]', 'WR [1]'])

# Plot trends in free variables
fitness, free_vars = dh.get_archive_data()
var_label = [
              '$\delta_e$ [m]', 
              "$r_ro$ [m]",
              r'$\alpha_{st}$ [deg]', 
              '$d_{so}$ [m]',
              '$w_{st}$ [m]',
              '$d_{st}$ [m]',
              '$d_{sy}$ [m]',
              r'$\alpha_m$ [deg]',
              '$d_m$ [m]',
              '$d_{mp}$ [m]',
              '$d_{ri}$ [m]',
            ]

bp2 = (0.00275, 0.01141, 44.51, 5.43e-3, 9.09e-3, 16.94e-3, 13.54e-3, 180.0, 3.41e-3, 1e-3, 3e-3,)
# # bounds for pygmo optimization problem
bounds = [
    [0.5 * bp2[0], 2 * bp2[0]],  # delta_e
    [0.5 * bp2[1], 2 * bp2[1]],  # r_ro    this will change the tip speed
    [0.2 * bp2[2], 1.1 * bp2[2]],  # alpha_st
    [0.2 * bp2[3], 2 * bp2[3]],  # d_so
    [0.2 * bp2[4], 3 * bp2[4]],  # w_st
    [0.5 * bp2[5], 2 * bp2[5]],  # d_st
    [0.5 * bp2[6], 2 * bp2[6]],  # d_sy
    [0.99 * bp2[7], 1 * bp2[7]],  # alpha_m
    [0.2 * bp2[8], 2 * bp2[8]],  # d_m
    [0 * bp2[9], 1 * bp2[9]],  # d_mp
    [0.3 * bp2[10], 2 * bp2[10]],  # d_ri
]
da.plot_x_with_bounds(free_vars, var_label, bounds)

dh.select_designs()

# proj_120_ = dh.get_design( 'proj_97_')
# print("proj_120_ d_st", proj_120_.machine.d_st)
