import os
import sys

from SynR_architect import AM_SynR_Architect
from mach_eval.machines.materials.electric_steels import Arnon5
from mach_eval.machines.materials.AM_materials import (
    Fe3Si,
    L316,
)
from mach_eval.machines.materials.miscellaneous_materials import (
    Copper,
    Air,
)
from SynR_settings_handler import AM_SynR_Settings_Handler
from mach_eval import MachineDesigner

# Specify machine specifications
AM_SynR_parameters = {
    'p': 2,
    'Q': 12,
    'rated_speed': 1800,
    'rated_current': 20,   
}

AM_SynR_materials = {
    "air_mat": Air,
    "rotor_iron_mat": Fe3Si,
    "rotor_barrier_mat": L316,
    "stator_iron_mat": Arnon5,
    "coil_mat": Copper,
    "shaft_mat": L316,
}

AM_SynR_winding = {
    "no_of_layers": 2,
    "layer_phases": [ ['U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V'],
                        ['W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U', 'W', 'V', 'U'] ],
    "layer_polarity": [ ['+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-'],
                        ['-', '+', '-', '+', '-', '+', '-', '+', '-', '+', '-', '+'] ],
    "pitch": 2,
    "Z_q": 20,
    "Kov": 1.8,
    "Kcu": 0.5,
    "phase_current_offset": 0,
}


# initialize BSPMArchitect with machine specification
arch = AM_SynR_Architect(AM_SynR_parameters, AM_SynR_materials, AM_SynR_winding)
set_handler = AM_SynR_Settings_Handler()

designer = MachineDesigner(arch, set_handler)