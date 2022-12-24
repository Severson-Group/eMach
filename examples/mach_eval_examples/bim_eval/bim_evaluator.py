import os
import sys
from time import time as clock_time

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")
sys.path.append(os.path.dirname(__file__))

from mach_eval import MachineEvaluator
from time_harmonic_step import time_harmonic_step
from transient_2tss_step import transient_2tss_step

############################ Create Evaluator ########################
bim_evaluator = MachineEvaluator(
    [
        time_harmonic_step,
        transient_2tss_step
    ]
)

from mach_eval import MachineDesign
# from example_machine import example_machine, machine_op_pt
from example_machine_2 import example_machine, machine_op_pt

design_variant = MachineDesign(example_machine, machine_op_pt)

tic = clock_time()
results = bim_evaluator.evaluate(design_variant)
toc = clock_time()

print("Time spent on BIM evaluation is %g min." % ((toc- tic)/60))

x = 4