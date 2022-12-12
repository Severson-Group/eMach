import os
import sys

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")
print(os.path.dirname(__file__)+"/../../..")

from mach_eval.machines.materials.electric_steels import (M19Gauge29, Arnon5)
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
    'alpha_st': 11,
    'alpha_so': 0,
    'r_si': 34.45,
    'd_so': 2.61,
    'd_sp': 3.95,
    'd_st': 20.75,
    'd_sy': 15.84,
    'w_st': 5.38,
    'r_ri': 7.48,
    'r_sh': 7.48,
    'd_ri': 18.77,
    'r_rb': 2.54,
    'd_rso': 0.47,
    'w_so': 0.86,
    'l_st': 50,
}


bim_parameters = {
    'p': 1,
    'ps': 2,
    'Q': 24,
    'Qr': 16,
    "name": "example_machine_2",
    'n_m': 1,
    'rated_speed': 29250,
    'rated_power': 3584,
    'rated_voltage': 48,
    'rated_current': 8.93,  
}

Aluminum = {
    'rotor_bar_material': 'Aluminium',
    'bar_conductivity': 46237525, #47619047.61904761,
    'bar_material_density': 2710 # kg/m^3
}
Copper = {
    'coil_material'              : 'Copper',
    'copper_elec_conductivity': 5.7773*1e7
}
# M19Gauge29 = {
#     'core_material'              : 'M19Gauge29',
#     'core_material_density'      : 7650, # kg/m3
#     'core_youngs_modulus'        : 185E9, # Pa
#     'core_poission_ratio'        : .3,
#     'core_material_cost'         : 17087, # $/m3
#     'core_ironloss_a'            : 2,
#     'core_ironloss_b'            : 1,
#     'core_ironloss_Kh'           : 143, # W/m3
#     'core_ironloss_Ke'           : 0.53, # W/m3
#     'core_therm_conductivity'    : 25, # W/m-k
#     'core_stacking_factor'       : 96, # percentage
#     'core_bh_file'               : os.path.dirname(__file__) + '/M-19-Steel-BH-Curve-afterJMAGsmooth.BH',
#     }

bim_materials = {
    "air_mat": Air,
    "rotor_iron_mat": Arnon5,
    "stator_iron_mat": Arnon5,
    "rotor_bar_mat": Aluminum,
    "coil_mat": Copper,
    "shaft_mat": Steel,
}

# DPNV:
    # "layer_phases": [ ['U', 'U', 'U', 'W', 'W', 'W', 'W', 'V', 'V', 'V', 'V', 'U', 'U', 'U', 'U', 'W', 'W',
    #                                'W', 'W', 'V', 'V', 'V', 'V', 'U'],
    #                     ['W', 'W', 'W', 'W', 'V', 'V', 'V', 'V', 'U', 'U', 'U', 'U', 'W', 'W', 'W', 'W', 'V',
    #                                  'V', 'V', 'V', 'U', 'U', 'U', 'U'] ],
    # "layer_polarity": [ ['+', '+', '+', '-', '-', '-', '-', '+', '+', '+', '+', '-', '-', '-', '-', '+', '+',
    #                               '+', '+', '-', '-', '-', '-', '+'],
    #                     ['-', '-', '-', '-', '+', '+', '+', '+', '-', '-', '-', '-', '+', '+', '+', '+', '-',
    #                                 '-', '-', '-', '+', '+', '+', '+'] ],

bim_winding = {
    "no_of_phases": 6,
    "no_of_layers": 2,
    "name_phases": ['Ph1', 'Ph2', 'Ph3', 'Ph4', 'Ph5', 'Ph6'],
    # layer_phases is a list of lists, the number of lists = no_of_layers
    # first list corresponds to coil sides in first layer
    # second list corresponds to coil sides in second layer
    # the index indicates the slot opening corresponding to the coil side
    # string characters are used to represent the phases
    "layer_phases": [ ['Ph1', 'Ph1', 'Ph2', 'Ph2', 'Ph2', 'Ph2', 'Ph3', 'Ph3', 'Ph3', 'Ph3', 'Ph4', 'Ph4', 'Ph4', 'Ph4', 'Ph5', 'Ph5',
                                   'Ph5', 'Ph5', 'Ph6', 'Ph6', 'Ph6', 'Ph6', 'Ph1', 'Ph1'],
                        ['Ph5', 'Ph5', 'Ph5', 'Ph6', 'Ph6', 'Ph6', 'Ph6', 'Ph1', 'Ph1', 'Ph1', 'Ph1', 'Ph2', 'Ph2', 'Ph2', 'Ph2', 'Ph3', 'Ph3', 'Ph3',
                                     'Ph3', 'Ph4', 'Ph4', 'Ph4', 'Ph4', 'Ph5'] ],
    # layer_polarity is a list of lists, the number of lists = no_of_layers
    # first list corresponds to coil side direction in first layer
    # second list corresponds to coil side direction in second layer
    # the index indicates the slot opening corresponding to the coil side
    # + indicates coil side goes into the page, - indicates coil side comes out of page
    "layer_polarity": [ ['+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+',
                                  '+', '+', '+', '+', '+', '+', '+'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                                    '-', '-', '-', '-', '-', '-', '-'] ],
    "pitch": 9,
    "Z_q": 16,
    "Kov": 1.8,
    "Kcu": 0.5,
    "phase_current_offset": 0,
    "no_of_layers_rotor": 1,
    "name_phases_rotor": ['PhR1', 'PhR2', 'PhR3', 'PhR4', 'PhR5', 'PhR6', 'PhR7', 'PhR8'],
    "layer_phases_rotor": [['PhR1', 'PhR2', 'PhR3', 'PhR4', 'PhR5', 'PhR6', 'PhR7', 'PhR8',
                            'PhR1', 'PhR2', 'PhR3', 'PhR4', 'PhR5', 'PhR6', 'PhR7', 'PhR8']],
    "layer_polarity_rotor": [['+', '+', '+', '+', '+', '+', '+', '+',
                            '-', '-', '-', '-', '-', '-', '-', '-']],
    "Z_q_rotor": 1,
    'no_of_phases_rotor': 8,
    "Kov_rotor": 1.6,
}

example_machine = BIM_Machine(
    bim_dimensions, bim_parameters, bim_materials, bim_winding
)

################ DEFINE BIM operating point ################
machine_op_pt = BIM_Machine_Oper_Pt(
    speed=29250,
    # slip_freq=12.5,
    It_hat = 8.93,
    Is_hat = 1.14,
    phi_t_0 = 0,
    phi_s_0 = 0,
    ambient_temp=25,
    rotor_temp_rise=55,
)
