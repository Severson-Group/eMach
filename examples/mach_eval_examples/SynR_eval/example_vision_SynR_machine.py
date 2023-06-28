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
from mach_eval.machines.SynR.Vision_SynR_machine import Vision_SynR_Machine
from mach_eval.machines.SynR.Vision_SynR_machine_oper_pt import Vision_SynR_Machine_Oper_Pt

################ DEFINE SynR Machine ################
SynR_dimensions = {
    'alpha_b': 135,
    'r_sh': 6,
    'r_ri': 6,
    'r_ro': 50,
    'r_f1': 0.1,
    'r_f2': 0.1,
    'r_f3': 0.1,
    'd_r1': 8,
    'd_r2': 8,
    'd_r3': 8,
    'w_b1': 4,
    'w_b2': 4,
    'w_b3': 4,
    'l_b1': 29.5,
    'l_b2': 20.5,
    'l_b3': 8.5,
    'l_b4': 20,
    'l_b5': 15,
    'l_b6': 10,
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
    "name": "Example_Vision_SynR_Machine",
    'rated_speed': 1800,
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

Example_Vision_SynR_Machine = Vision_SynR_Machine(
    SynR_dimensions, SynR_parameters, SynR_materials, SynR_winding
)

################ DEFINE SynR operating point ################
Vision_Machine_Op_Pt = Vision_SynR_Machine_Oper_Pt(
    speed=1800,
    current_ratio=1,
    phi_0 = 0,
    ambient_temp=25,
    rotor_temp_rise=0,
)