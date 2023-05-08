import os
import sys
import numpy as np

from mach_eval.machines.materials.electric_steels import (Arnon5)
from mach_eval.machines.materials.miscellaneous_materials import (
    Steel,
    Copper,
    Air,
)
from mach_eval.machines.materials.AM_materials import (
    Fe3Si,
    L316,
)
from mach_eval.machines.SynR.AM_SynR_machine import AM_SynR_Machine
from mach_eval.machines.SynR.AM_SynR_machine_oper_pt import AM_SynR_Machine_Oper_Pt

################ DEFINE AM SynR Machine ################
SynR_dimensions = {
    'r_sh': 6,
    'r_ri': 6,
    'r_ro': 49,
    'd_r1': 8,
    'd_r2': 8,
    'w_b1': 4,
    'w_b2': 4,
    'alpha_st': 25,
    'alpha_so': 12.5,
    'r_si': 50,
    'd_so': 5,
    'd_sp': 9,
    'd_st': 40,
    'd_sy': 36,
    'w_st': 12,
    'l_st': 100,
}

SynR_parameters = {
    'p': 2,
    'Q': 12,
    "name": "Example_SynR_Machine",
    'rated_speed': 1800,
    'rated_current': 20,   
}

SynR_materials = {
    "air_mat": Air,
    "rotor_iron_mat": Fe3Si,
    "rotor_barrier_mat": L316,
    "stator_iron_mat": Arnon5,
    "coil_mat": Copper,
    "shaft_mat": Steel,
}

SynR_winding = {
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

Example_AM_SynR_Machine = AM_SynR_Machine(
    SynR_dimensions, SynR_parameters, SynR_materials, SynR_winding
)

################ DEFINE SynR operating point ################
Machine_Op_Pt = AM_SynR_Machine_Oper_Pt(
    speed=1800,
    current_ratio=1,
    phi_0 = 0,
    ambient_temp=25,
    rotor_temp_rise=0,
)