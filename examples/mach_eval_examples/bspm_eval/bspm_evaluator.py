import os
import sys

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")
sys.path.append(os.path.dirname(__file__))

from mach_eval import MachineEvaluator
from structural_step import struct_step
from electromagnetic_step import em_step
from rotor_thermal_step import rotor_therm_step
from stator_thermal_step import stator_therm_step
from windage_loss_step import windage_step

############################ Create Evaluator ########################
evaluator = MachineEvaluator(
    [
        struct_step,
        em_step,
        rotor_therm_step,
        stator_therm_step,
        windage_step,
    ]
)


# evaluate example design if script is run
if __name__ == "__main__":
    from ecce_2020_bspm import ecce_2020_machine, ecce_2020_op_pt
    from mach_eval import MachineDesign

    ecce_2020_design = MachineDesign(ecce_2020_machine, ecce_2020_op_pt)
    results = evaluator.evaluate(ecce_2020_design)
