import os
import sys

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")
print(os.path.dirname(__file__)+"/../../..")

from mach_eval.machines.materials.electric_steels import Arnon5
from mach_eval.machines.materials.jmag_library_magnets import N40H
from mach_eval.machines.materials.miscellaneous_materials import (
    CarbonFiber,
    Steel,
    Copper,
    Hub,
    Air,
)
from mach_eval.machines.bspm import BSPM_Machine
from mach_eval.machines.bspm.bspm_oper_pt import BSPM_Machine_Oper_Pt

################ DEFINE BP2 ################
bspm_dimensions = {
    'alpha_st': 44.5,
    'd_so': 0.00542,
    'w_st': 0.00909,
    'd_st': 0.0169,
    'd_sy': 0.0135,
    'alpha_m': 178.78,
    'd_m': 0.00371,
    'd_mp': 0.00307,
    'd_ri': 0.00489,
    'alpha_so': 22.25,
    'd_sp': 0.00813,
    'r_si': 0.01416,
    'alpha_ms': 178.78,
    'd_ms': 0,
    'r_sh': 0.00281,
    'l_st': 0.0115,
    'd_sl': 0.00067,
    'delta_sl': 0.00011
}

bspm_parameters = {
    'p': 1,
    'ps': 2,
    'n_m': 1,
    'Q': 6,
    'rated_speed': 16755.16,
    'rated_power': 5500.0,
    'rated_voltage': 240,
    'rated_current': 10.0,
    "name": "ECCE2020"
}

bspm_materials = {
    "air_mat": Air,
    "rotor_iron_mat": Arnon5,
    "stator_iron_mat": Arnon5,
    "magnet_mat": N40H,
    "rotor_sleeve_mat": CarbonFiber,
    "coil_mat": Copper,
    "shaft_mat": Steel,
    "rotor_hub": Hub,
}

bspm_winding = {
    "no_of_layers": 2,
    # layer_phases is a list of lists, the number of lists = no_of_layers
    # first list corresponds to coil sides in first layer
    # second list corresponds to coil sides in second layer
    # the index indicates the slot opening corresponding to the coil side
    # string characters are used to represent the phases
    "layer_phases": [ ['U', 'W', 'V', 'U', 'W', 'V'],
                        ['W', 'V', 'U', 'W', 'V', 'U'] ],
    # layer_polarity is a list of lists, the number of lists = no_of_layers
    # first list corresponds to coil side direction in first layer
    # second list corresponds to coil side direction in second layer
    # the index indicates the slot opening corresponding to the coil side
    # + indicates coil side goes into the page, - indicates coil side comes out of page
    "layer_polarity": [ ['+', '-', '+', '-', '+', '-'],
                        ['-', '+', '-', '+', '-', '+'] ],
    # coil_groups are a unique property of DPNV windings
    # coil group is assigned corresponding to the 1st winding layer
    "coil_groups": ['b', 'a', 'b', 'a', 'b', 'a'],
    "pitch": 2,
    "Z_q": 49,
    "Kov": 1.8,
    "Kcu": 0.5,
    "phase_current_offset": 0 
}

ecce_2020_machine = BSPM_Machine(
    bspm_dimensions, bspm_parameters, bspm_materials, bspm_winding
)

################ DEFINE BP2 operating point ################
ecce_2020_op_pt = BSPM_Machine_Oper_Pt(
    Id=0,
    Iq=0.975,
    Ix=0,
    Iy=0.025,
    speed=160000,
    ambient_temp=25,
    rotor_temp_rise=55,
)
