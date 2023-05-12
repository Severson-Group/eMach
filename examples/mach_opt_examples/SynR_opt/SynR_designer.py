import os
import sys

# change current working directory to file location
sys.path.append(os.path.dirname(__file__)+"/../../..")

from SynR_architect import SynR_Architect1
from mach_eval.machines.materials.electric_steels import Arnon5
from mach_eval.machines.materials.AM_materials import (
    Fe3Si,
    L316,
)
from mach_eval.machines.materials.miscellaneous_materials import (
    Copper,
    Air,
)
from SynR_settings_handler import SynR_Settings_Handler
from mach_eval import MachineDesigner

# specify machine specs
design_spec = {
    "p": 2,
    "Q": 12,
    "name": "Example_SynR_Machine",
    "rated_speed": 1800,
    "rated_current": 20,   
}

materials = {
    "air_mat": Air,
    "rotor_iron_mat": Fe3Si,
    "rotor_barrier_mat": L316,
    "stator_iron_mat": Arnon5,
    "coil_mat": Copper,
    "shaft_mat": L316,
}

# initialize BSPMArchitect with machine specification
arch = SynR_Architect1(design_spec, materials)
set_handler = SynR_Settings_Handler()

designer = MachineDesigner(arch, set_handler)