import os
import sys

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")

from bspm_designer import designer
from examples.mach_eval_examples.bspm_eval.bspm_evaluator import evaluator
from bspm_ds import BSPMDesignSpace
from mach_opt import DesignProblem, DesignOptimizationMOEAD
from my_data_handler import MyDataHandler

# run optimization
bp2 = (
    0.00275,
    0.01141,
    44.51,
    5.43e-3,
    9.09e-3,
    16.94e-3,
    13.54e-3,
    180.0,
    3.41e-3,
    1e-3,
    3e-3,
)

# set bounds for pygmo optimization problem
bounds = [
    [0.9 * bp2[0], 1.1 * bp2[0]],  # delta_e
    [1 * bp2[1], 1.1 * bp2[1]],  # r_ro    this will change the tip speed
    [0.9 * bp2[2], 1.1 * bp2[2]],  # alpha_st
    [0.9 * bp2[3], 1.1 * bp2[3]],  # d_so
    [0.9 * bp2[4], 1.1 * bp2[4]],  # w_st
    [0.9 * bp2[5], 1.1 * bp2[5]],  # d_st
    [0.9 * bp2[6], 1.1 * bp2[6]],  # d_sy
    [0.99 * bp2[7], 1 * bp2[7]],  # alpha_m
    [1 * bp2[8], 1.1 * bp2[8]],  # d_m
    [0 * bp2[9], 1 * bp2[9]],  # d_mp
    [0.3 * bp2[10], 1 * bp2[10]],  # d_ri
]

path = os.path.dirname(__file__)
arch_file = path + r"\opti_arch.pkl"  # specify path where saved data will reside
des_file = path + r"\opti_designer.pkl"
pop_file = path + r"\latest_pop.csv"
dh = MyDataHandler(arch_file, des_file)  # initialize data handler with required file paths

opt_settings = BSPMDesignSpace(3, bounds)
design_prob = DesignProblem(designer, evaluator, opt_settings, dh)
design_opt = DesignOptimizationMOEAD(design_prob)

pop_size = 78
gen_size = 10


population = design_opt.load_pop(filepath=pop_file, pop_size=78)
if population is None:
    print("NO EXISTING POPULATION TO LOAD")
    population = design_opt.initial_pop(pop_size)
pop = design_opt.run_optimization(population, gen_size, pop_file)
