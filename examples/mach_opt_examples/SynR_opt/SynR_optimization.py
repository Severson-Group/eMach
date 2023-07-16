import os
import sys

os.chdir(os.path.dirname(__file__))
sys.path.append("../../../")

from mach_opt import DesignProblem, DesignOptimizationMOEAD
from mach_eval import MachineEvaluator
from examples.mach_opt_examples.SynR_opt.my_data_handler import MyDataHandler
from SynR_designer import designer
from SynR_ds import AMSynRDesignSpace
from examples.mach_eval_examples.SynR_eval.optimization_AM_step import optimization_AM_step
from time import time as clock_time

AM_SynR_evaluator = MachineEvaluator(
    [
        optimization_AM_step,
    ]
)

# set bounds for pygmo optimization problem
dims = (
    6.35,
    50,
    8,
    8,
    4,
    4,
)

bounds = [
    [0.999 * dims[0], 1 * dims[0]],  # r_ri
    [0.9 * dims[1], 1 * dims[1]],  # r_ro
    [0.5 * dims[2], 2 * dims[2]],  # d_r1
    [0.5 * dims[3], 2 * dims[3]],  # d_r2
    [0.5 * dims[4], 2 * dims[4]],  # w_b1
    [0.5 * dims[5], 2 * dims[5]],  # w_b2
]

n_obj = 3

# create optimization Design Space object
opt_settings = AMSynRDesignSpace(n_obj, bounds)

# create optimization Data Handler
path = os.path.dirname(__file__)
arch_file = path + r"\opti_arch.pkl"  # specify file where archive data will reside
des_file = path + r"\opti_designer.pkl"
pop_file = path + r"\latest_pop.csv"  # csv file holding free variables of latest population
dh = MyDataHandler(arch_file, des_file)  # initialize data handler with required file paths

# create pygmo Problem
design_prob = DesignProblem(designer, AM_SynR_evaluator, opt_settings, dh)
# define pygmo MOEAD optimization
design_opt = DesignOptimizationMOEAD(design_prob)

# define population size and number of generations
pop_size = 66
gen_size = 2 # CHANGE ONCE OPTIMIZATION IS FINALIZED!

# load latest population
population = design_opt.load_pop(filepath=pop_file, pop_size=pop_size)
# create random initial population if no prior data exists
if population is None:
    print("NO EXISTING POPULATION TO LOAD")
    population = design_opt.initial_pop(pop_size)

# RUN OPTIMIZATION
tic = clock_time()
pop = design_opt.run_optimization(population, gen_size, pop_file)
toc = clock_time()
print("Time spent on AM SynR optimization is %g hours." % ((toc- tic)/3600))