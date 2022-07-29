import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../../..")

from bspm_architect import BSPM_Architect1
from mach_eval.machines.bspm_specification import BSPMMachineSpec
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
    "rated_power": 11e3,  # rated power in W
    "voltage_rating": 240,  # line-line voltage rating
}
# define BSPM machine specification object
machine_spec = BSPMMachineSpec(
    design_spec=design_spec,
    rotor_core=Arnon5,
    stator_core=Arnon5,
    magnet=N40H,
    conductor=Copper,
    shaft=Steel,
    air=Air,
    sleeve=CarbonFiber,
    hub=Hub,
)

# initialize BSPMArchitect with machine specification
arch = BSPM_Architect1(machine_spec)
set_handler = BSPM_Settings_Handler()

designer = MachineDesigner(arch, set_handler)
