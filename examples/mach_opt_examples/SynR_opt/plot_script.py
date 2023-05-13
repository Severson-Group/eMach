#%% 
import os
import numpy as np
import pandas as pd
import sys

sys.path.append(os.path.dirname(__file__))
from my_data_handler import MyDataHandler
from my_plotting_functions import DataAnalyzer

path = os.path.dirname(__file__)
arch_file = path + r'/opti_arch.pkl'  # specify path where saved data will reside
des_file = path + r'/opti_designer.pkl'
dh = MyDataHandler(arch_file, des_file)  # initialize data handler with required file paths
da = DataAnalyzer(path)

fitness, free_vars = dh.get_pareto_fitness_freevars()
fts = np.asarray(fitness)
   
fitness_dict = {'PRV': fts[:,0],
                'eff': fts[:,1],
                'Trip': fts[:,2],}
fitness_df = pd.DataFrame.from_dict(fitness_dict)
if os.path.exists('fitness.csv') == False:
    fitness_df.to_csv('fitness.csv')

#%% Plot Pareto Front
da.plot_pareto_front(points=fitness, label=['-PRV [kW/m$^3$]', '-$\eta$ [%]', '$T_{rip}$'])

#%% Plot trends in free variables
fitness, free_vars = dh.get_archive_data()
var_label = [
              '$r_{ri}$ [mm]', 
              "$r_{ro}$ [mm]",
              '$d_{r1}$ [mm]',
              '$d_{r2}$ [mm]',
              '$w_{b1}$ [mm]',
              '$w_{b2}$ [mm]',
            ]

dims = (
    6,
    49.5,
    8,
    8,
    4,
    4,
)

bounds = [
    [0.5 * dims[0], 2 * dims[0]],  # r_ri
    [0.9 * dims[1], 1 * dims[1]],  # r_ro
    [0.5 * dims[2], 2 * dims[2]],  # d_r1
    [0.5 * dims[3], 2 * dims[3]],  # d_r2
    [0.5 * dims[4], 2 * dims[4]],  # w_b1
    [0.5 * dims[5], 2 * dims[5]],  # w_b2
]

da.plot_x_with_bounds(free_vars, var_label, bounds)

# check designs which meet required specs
dh.select_designs()

# proj_1_ selected based on performance (CHANGE TO PROJECT XXXX BASED ON PERFORMANCE)
proj_name = 'proj_'
# load proj_1_ design from archive (CHANGE TO PROJECT XXXX BASED ON PERFORMANCE)
proj_1_ = dh.get_design(proj_name)
print(proj_name, "d_st =", proj_1_.machine.d_st)

# save proj_1_ to pickle file (CHANGE TO PROJECT XXXX BASED ON PERFORMANCE)
object_filename = path + "/" + proj_name + r'.pkl'
dh.save_object(proj_1_, object_filename)

# read proj_1_ design from pickle file (CHANGE TO PROJECT XXXX BASED ON PERFORMANCE)
proj_read = dh.load_object(object_filename)
print("From pickle file, d_st =", proj_read.machine.d_st)