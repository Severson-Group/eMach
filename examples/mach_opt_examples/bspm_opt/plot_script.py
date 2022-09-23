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

dims = (0.003, 0.012, 45, 5.5e-3, 9e-3, 17e-3, 13.5e-3, 180.0, 3e-3, 1e-3, 3e-3)
# # bounds for pygmo optimization problem
bounds = [
    [0.5 * dims[0], 2 * dims[0]],  # delta_e
    [0.5 * dims[1], 2 * dims[1]],  # r_ro    this will change the tip speed
    [0.2 * dims[2], 1.1 * dims[2]],  # alpha_st
    [0.2 * dims[3], 2 * dims[3]],  # d_so
    [0.2 * dims[4], 3 * dims[4]],  # w_st
    [0.5 * dims[5], 2 * dims[5]],  # d_st
    [0.5 * dims[6], 2 * dims[6]],  # d_sy
    [0.99 * dims[7], 1 * dims[7]],  # alpha_m
    [0.2 * dims[8], 2 * dims[8]],  # d_m
    [0 * dims[9], 1 * dims[9]],  # d_mp
    [0.3 * dims[10], 2 * dims[10]],  # d_ri
]
da.plot_x_with_bounds(free_vars, var_label, bounds)

# check designs which meet required specs
dh.select_designs()

# proj_1207_ selected based on performance
proj_name = 'proj_1207_'
# load proj_1207_ design from archive
proj_1207_ = dh.get_design( proj_name)
print(proj_name, "d_st =", proj_1207_.machine.d_st)

# save proj_1207_ to pickle file
object_filename = path + "/" + proj_name + r'.pkl'
dh.save_object(proj_1207_, object_filename)

# read proj_1207_ design from pickle file
proj_read = dh.load_object(object_filename)
print("From pickle file, d_st =", proj_read.machine.d_st)