import os
import sys

# change current working directory to file location
sys.path.append(os.path.dirname(__file__)+"/../../..")

from bim_architect import BIM_Architect
from mach_eval.machines.materials.electric_steels import (
    Arnon5,
    M19Gauge29,
)
from mach_eval.machines.materials.miscellaneous_materials import (
    Steel,
    # Copper,
    Air,
)
from bim_settings_handler import BIM_Settings_Handler
from mach_eval import MachineDesigner

# Specify machine specifications
bim_parameters = {
    'p': 1,
    'ps': 2,
    'Q': 24,
    'Qr': 16,
    'n_m': 1,
    'rated_speed': 30000, # RPM
    'rated_power': 50000,
    'rated_voltage': 480,
    # 'rated_current': 8.93,
    'rated_speed_m_s': 150, # m/s
    "J": 4e6,  # Arms/m^2
    "Jr": 6.5e6,  # Arms/m^2
    "wire_area": 2 * 1e-6,  # cross-sectional area of a conductor [m^2]
}

# bim_dimensions = {
#     'r_ri': 7.515,
# }


Aluminum = {
    'rotor_bar_material': 'Aluminium',
    'bar_conductivity': 46237525, #47619047.61904761,
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
    "layer_phases": [ ['Ph1', 'Ph1', 'Ph2', 'Ph2', 'Ph2', 'Ph2', 'Ph3', 'Ph3', 'Ph3', 'Ph3', 'Ph4', 'Ph4', 'Ph4', 'Ph4', 'Ph5', 'Ph5',
                                   'Ph5', 'Ph5', 'Ph6', 'Ph6', 'Ph6', 'Ph6', 'Ph1', 'Ph1'],
                        ['Ph5', 'Ph5', 'Ph5', 'Ph6', 'Ph6', 'Ph6', 'Ph6', 'Ph1', 'Ph1', 'Ph1', 'Ph1', 'Ph2', 'Ph2', 'Ph2', 'Ph2', 'Ph3', 'Ph3', 'Ph3',
                                     'Ph3', 'Ph4', 'Ph4', 'Ph4', 'Ph4', 'Ph5'] ],
    "layer_polarity": [ ['+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+',
                                  '+', '+', '+', '+', '+', '+', '+'],
                        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                                    '-', '-', '-', '-', '-', '-', '-'] ],
    "pitch": 9,
    # "Z_q": 16,
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


# initialize BSPMArchitect with machine specification
arch = BIM_Architect(bim_parameters, bim_materials, bim_winding)
set_handler = BIM_Settings_Handler()

designer = MachineDesigner(arch, set_handler)
