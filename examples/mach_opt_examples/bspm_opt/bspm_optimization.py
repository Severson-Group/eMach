import os
import sys

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")

from bspm_designer import designer
from examples.mach_eval_examples.bspm_eval.bspm_evaluator import evaluator
from bspm_ds import BSPMDesignSpace
from mach_opt import DesignProblem, DesignOptimizationMOEAD
from my_data_handler import MyDataHandler

# set bounds for pygmo optimization problem
dims = (
    0.003,
    0.012,
    45,
    5.5e-3,
    9e-3,
    17e-3,
    13.5e-3,
    180.0,
    3e-3,
    1e-3,
    3e-3,
)

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

# create optimization Design Space object
opt_settings = BSPMDesignSpace(3, bounds)

# create optimization Data Handler
path = os.path.dirname(__file__)
arch_file = path + r"\opti_arch.pkl"  # specify file where archive data will reside
des_file = path + r"\opti_designer.pkl"
pop_file = path + r"\latest_pop.csv"  # csv file holding free variables of latest population
dh = MyDataHandler(arch_file, des_file)  # initialize data handler with required file paths

# create pygmo Problem
design_prob = DesignProblem(designer, evaluator, opt_settings, dh)
# defin pygmo MOEAD optimization
design_opt = DesignOptimizationMOEAD(design_prob)

# define population size and number of generations
pop_size = 78
gen_size = 20

# load latest population
population = design_opt.load_pop(filepath=pop_file, pop_size=78)
# create random initial population if no prior data exists
if population is None:
    print("NO EXISTING POPULATION TO LOAD")
    population = design_opt.initial_pop(pop_size)

# RUN OPTIMIZATION
pop = design_opt.run_optimization(population, gen_size, pop_file)
