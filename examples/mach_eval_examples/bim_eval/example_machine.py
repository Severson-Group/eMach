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
    # Copper,
    Hub,
    Air,
)
from mach_eval.machines.bim.bim_machine import BIM_Machine
from mach_eval.machines.bim.bim_oper_pt import BIM_Machine_Oper_Pt

bim_dimensions = {
    'alpha_st': 9.624,
    'alpha_so': 0,
    'r_si': 50.18446292756861,
    'd_so': 0.2892842308933503,
    'd_sp': 0.5785684617867006,
    'd_st': 27.176968610644685,
    'd_sy': 35.827,
    'w_st': 10.240361002369372,
    'r_ri': 8.909627424964462,
    'r_sh': 8.909627424964462,
    'd_ri': 34.31782508867679,
    'r_rb': 1.6699405702001604,
    'd_rso': 1.1791492735270337,
    'w_so': 1.0010737572184039,
    'l_st': 92.5925925,
}


bim_parameters = {
    'p': 1,
    'ps': 2,
    'Q': 24,
    'Qr': 32,
    "name": "example_machine",
    'n_m': 1,
    'rated_speed': 8645,
    'rated_power': 50e3,
    'rated_voltage': 480,
    'rated_current': 127.89733 / 2,  
}

Aluminum = {
    'rotor_bar_material': 'Aluminium',
    'bar_conductivity': 3.7665e+07, # 47619047.61904761
    'bar_material_density': 2710 # kg/m^3
}
Copper = {
    'coil_material'              : 'Copper',
    'copper_elec_conductivity': 5.7773*1e7
}
bim_materials = {
    "air_mat": Air,
    "rotor_iron_mat": Arnon5,
    "stator_iron_mat": Arnon5,
    "rotor_bar_mat": Aluminum,
    "coil_mat": Copper,
    "shaft_mat": Steel,
}

bim_winding = {
    "no_of_phases": 6,
    "no_of_layers": 2,
    "name_phases": ['Ph1', 'Ph2', 'Ph3', 'Ph4', 'Ph5', 'Ph6'],
    "layer_phases": [ ['Ph1', 'Ph1', 'Ph1', 'Ph2', 'Ph2', 'Ph2', 'Ph2', 'Ph3', 'Ph3', 'Ph3', 'Ph3', 'Ph4', 'Ph4', 'Ph4', 'Ph4', 'Ph5', 'Ph5',
                                   'Ph5', 'Ph5', 'Ph6', 'Ph6', 'Ph6', 'Ph6', 'Ph1'],
                        ['Ph5', 'Ph5', 'Ph5', 'Ph5', 'Ph6', 'Ph6', 'Ph6', 'Ph6', 'Ph1', 'Ph1', 'Ph1', 'Ph1', 'Ph2', 'Ph2', 'Ph2', 'Ph2', 'Ph3',
                                     'Ph3', 'Ph3', 'Ph3', 'Ph4', 'Ph4', 'Ph4', 'Ph4'] ],
    "layer_polarity": [ ['+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+',
                                  '+', '+', '+', '+', '+', '+', '+'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                                    '-', '-', '-', '-', '-', '-', '-'] ],
    "pitch": 9,
    "Z_q": 49,
    "Kov": 1.8,
    "Kcu": 0.5,
    "phase_current_offset": 0, 
    "no_of_layers_rotor": 1,
    "name_phases_rotor": ['PhR1', 'PhR2', 'PhR3', 'PhR4', 'PhR5', 'PhR6', 'PhR7', 'PhR8',
                          'PhR9', 'PhR10', 'PhR11', 'PhR12', 'PhR13', 'PhR14', 'PhR15', 'PhR16'],
    "layer_phases_rotor": [['PhR1', 'PhR2', 'PhR3', 'PhR4', 'PhR5', 'PhR6', 'PhR7', 'PhR8', 'PhR9', 'PhR10', 'PhR11', 'PhR12',
        'PhR13', 'PhR14', 'PhR15', 'PhR16', 'PhR1', 'PhR2', 'PhR3', 'PhR4', 'PhR5', 'PhR6', 'PhR7', 'PhR8', 'PhR9', 
        'PhR10', 'PhR11', 'PhR12', 'PhR13', 'PhR14', 'PhR15', 'PhR16']],
    "layer_polarity_rotor": [['+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', 
                            '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']],
    "Z_q_rotor": 1,
    'no_of_phases_rotor': 16,
    "Kov_rotor": 1.6,
}

example_machine = BIM_Machine(
    bim_dimensions, bim_parameters, bim_materials, bim_winding
)

################ DEFINE BIM operating point ################
machine_op_pt = BIM_Machine_Oper_Pt(
    drive_freq=500,
    # slip_freq=1,
    It_hat = 0.975,
    Is_hat = 0.025,
    ambient_temp=25,
    rotor_temp_rise=55,
)
