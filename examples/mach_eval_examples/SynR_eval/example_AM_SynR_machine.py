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
    'r_ro': 50,
    'd_r1': 8,
    'd_r2': 8,
    'w_b1': 4,
    'w_b2': 4,
    'alpha_st': 7.5,
    'alpha_so': 3.75,
    'r_si': 50.5,
    'd_so': 1,
    'd_sp': 2,
    'd_st': 16.52,
    'd_sy': 9.39,
    'w_st': 3.25,
    'l_st': 70.61,
}

SynR_parameters = {
    'p': 2,
    'Q': 36,
    "name": "Example_SynR_Machine",
    'rated_speed': 60000,
    'rated_current': 4,   
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
    "layer_phases": [ ['U', 'U', 'U', 'W', 'W', 'W', 'V', 'V', 'V', 'U', 'U', 'U', 'W', 'W', 'W', 'V', 'V', 'V', 'U', 'U', 'U', 'W', 'W', 'W', 'V', 'V', 'V', 'U', 'U', 'U', 'W', 'W', 'W', 'V', 'V', 'V'],
                      ['U', 'U', 'W', 'W', 'W', 'V', 'V', 'V', 'U', 'U', 'U', 'W', 'W', 'W', 'V', 'V', 'V', 'U', 'U', 'U', 'W', 'W', 'W', 'V', 'V', 'V', 'U', 'U', 'U', 'W', 'W', 'W', 'V', 'V', 'V', 'U' ] ],
    "layer_polarity": [ ['+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-'],
                        ['+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+', '+', '+', '-', '-', '-', '+'] ],
    "pitch": 8,
    "Z_q": 36,
    "Kov": 1.8,
    "Kcu": 0.4,
    "phase_current_offset": 0,
}

Example_AM_SynR_Machine = AM_SynR_Machine(
    SynR_dimensions, SynR_parameters, SynR_materials, SynR_winding
)

################ DEFINE SynR operating point ################
Machine_Op_Pt = AM_SynR_Machine_Oper_Pt(
    speed=60000,
    current_ratio=1,
    phi_0 = 0,
    ambient_temp=25,
    rotor_temp_rise=0,
)