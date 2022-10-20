import os
import sys

# change current working directory to file location
sys.path.append(os.path.dirname(__file__)+"/../../..")

from bspm_architect import BSPM_Architect1
from mach_eval.machines.materials.electric_steels import Arnon5
from mach_eval.machines.materials.jmag_library_magnets import N40H
from mach_eval.machines.materials.miscellaneous_materials import (
    CarbonFiber,
    Steel,
    Copper,
    Hub,
    Air,
)
from bspm_settings_handler import BSPM_Settings_Handler
from mach_eval import MachineDesigner

# specify machine specs
design_spec = {
    "DPNV": True,
    "p": 1,
    "ps": 2,
    "Q": 6,
    "J": 5e6,  # Arms/m^2
    "wire_A": 2 * 1e-6,  # cross sectional area of conductors m^2
    "Kcu": 0.5,  # Stator slot fill/packing factor | FEMM_Solver.py is not consistent with this setting
    "Kov": 1.8,  # Winding over length factor
    "rated_speed": 16755.16,  # rated speed in ead/s
    "rated_power": 5.5e3,  # rated power in W
    "voltage_rating": 240,  # line-line voltage rating
}

materials = {
    "air_mat": Air,
    "rotor_iron_mat": Arnon5,
    "stator_iron_mat": Arnon5,
    "magnet_mat": N40H,
    "rotor_sleeve_mat": CarbonFiber,
    "coil_mat": Copper,
    "shaft_mat": Steel,
    "rotor_hub": Hub,
}
# initialize BSPMArchitect with machine specification
arch = BSPM_Architect1(design_spec, materials)
set_handler = BSPM_Settings_Handler()

designer = MachineDesigner(arch, set_handler)
