import os
import sys

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")

from bim_designer import designer, bim_parameters
from examples.mach_eval_examples.bim_eval.bim_evaluator import bim_evaluator
from bim_ds import BIMDesignSpace
from mach_opt import DesignProblem, DesignOptimizationMOEAD
from eMach.examples.mach_opt_examples.bim_opt.my_data_handler import MyDataHandler

# set bounds for pygmo optimization problem
dims = (
    1.44,
    7,
    360 / bim_parameters['Q'],
    2,
    22.8,
    31.7,
    2.5,
    2,
    2,
)

bounds = [
    [0.9 * dims[0], 2 * dims[0]],  # delta_e
    [0.5 * dims[1], 1.5 * dims[1]],  # w_st
    [0.2 * dims[2], 0.8 * dims[2]],  # alpha_st
    [0.25 * dims[3], 1.5 * dims[3]],  # d_so
    [0.8 * dims[4], 1.2 * dims[4]],  # d_st
    [0.8 * dims[5], 1.2 * dims[5]],  # d_sy
    [0.8 * dims[6], 1.2 * dims[6]],  # r_rb
    [0.25 * dims[7], 1.5 * dims[7]],  # w_so
    [0.25 * dims[8], 1.5 * dims[8]],  # d_rso
]

n_obj = 3

# create optimization Design Space object
opt_settings = BIMDesignSpace(n_obj, bounds)

# create optimization Data Handler
path = os.path.dirname(__file__)
arch_file = path + r"\opti_arch.pkl"  # specify file where archive data will reside
des_file = path + r"\opti_designer.pkl"
pop_file = path + r"\latest_pop.csv"  # csv file holding free variables of latest population
dh = MyDataHandler(arch_file, des_file)  # initialize data handler with required file paths

# create pygmo Problem
design_prob = DesignProblem(designer, bim_evaluator, opt_settings, dh)
# defin pygmo MOEAD optimization
design_opt = DesignOptimizationMOEAD(design_prob)

# define population size and number of generations
pop_size = 5 # 78
gen_size = 3 #100

# load latest population
population = design_opt.load_pop(filepath=pop_file, pop_size=78)
# create random initial population if no prior data exists
if population is None:
    print("NO EXISTING POPULATION TO LOAD")
    population = design_opt.initial_pop(pop_size)

# RUN OPTIMIZATION
pop = design_opt.run_optimization(population, gen_size, pop_file)
