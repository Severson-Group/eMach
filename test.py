import mach_eval.analyzers.electromagnetic.bspm.machine_constant.bspm_mach_constants as bmc
import mach_eval.analyzers.electromagnetic.bspm.machine_constant.bspm_mach_constants as bmc
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
from mach_eval.analyzers.electromagnetic.bspm.jmag_2d_config import JMAG_2D_Config
import os
import numpy as np

#########################################################
# CREATE BSPM MACHINE OBJECT
#########################################################

# **
# Actual machine does not have rotor core, only shaft.
# d_ri and r_sh are set to 0.1[mm] and 8.9[mm] respectively 
# to avoid InvalidDesign error. Actual shaft radius is 9[mm].
# Differences in results are negligble.

################ DEFINE BP4 ################
bspm_dimensions = {
    "alpha_st": 31.7088,   #[deg]
    "d_so": 2.02334e-3,     #[m]
    "w_st": 5.95805e-3,     #[m]
    "d_st": 18.4967e-3,     #[m]
    "d_sy": 5.81374e-3,     #[m]
    "alpha_m": 180,         #[m]
    "d_m": 3e-3,            #[m]
    "d_mp": 0,              #[m]
    "d_ri": 1e-3,         #[m]**  0.1e-3
    "alpha_so": 15.5,       #[deg] 
    "d_sp": 2.05e-3,        #[m]
    "r_si": 16.9737e-3,     #[m]
    "alpha_ms": 180,        #[deg]
    "d_ms": 0,              #[m]    
    "r_sh": 8e-3,         #[m]**  8.9e-3  
    "l_st": 25e-3,          #[m]
    "d_sl": 1e-3,           #[m]
    "delta_sl": 9.63e-5,    #[m] 
}

bspm_parameters = {
    "p": 1,     # number of pole pairs
    "ps": 2,    # number of suspension pole pairs
    "n_m": 1,   # 
    "Q": 6,     # number of slots
    "rated_speed": 16755.16,    #[rad/s] 
    "rated_power": 8e3,         # [W]   
    "rated_voltage": 8e3/18,   # [V_rms] 
    "rated_current": 10,      # [I_rms] #18
    "name": "BP4"
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
    "layer_phases": [["U", "W", "V", "U", "W", "V"], 
                     ["V", "U", "W", "V", "U", "W"]],
    # layer_polarity is a list of lists, the number of lists = no_of_layers
    # first list corresponds to coil side direction in first layer
    # second list corresponds to coil side direction in second layer
    # the index indicates the slot opening corresponding to the coil side
    # + indicates coil side goes into the page, - indicates coil side comes out of page
    "layer_polarity": [["+", "-", "+", "-", "+", "-"], 
                       ["+", "-", "+", "-", "+", "-"]],
    # coil_groups are a unique property of DPNV windings
    # coil group is assigned corresponding to the 1st winding layer
    "coil_groups": ["b", "a", "b", "a", "b", "a"],
    "pitch": 1,
    "Z_q": 45,
    "Kov": 1.8,
    "Kcu": 0.5,
    # add phase current offset to know relative rotor / current angle for creating Iq
    "phase_current_offset": -30  
}

bp4 = BSPM_Machine(
    bspm_dimensions, bspm_parameters, bspm_materials, bspm_winding
)

#########################################################
# DEFINE BSPM OPERATING POINT
#########################################################
bp4_op_pt = BSPM_Machine_Oper_Pt(
    Id=0,               # I_pu
    Iq=0.95,            # I_pu
    Ix=0,               # I_pu
    Iy=0.05,            # I_pu
    speed=160000,       # RPM
    ambient_temp=25,    # C
    rotor_temp_rise=55, # K
)

#########################################################
# DEFINE BSPM JMAG SETTINGS
#########################################################
jmag_config = JMAG_2D_Config(
    no_of_rev_1TS=2,
    no_of_rev_2TS=1,
    no_of_steps_per_rev_1TS=36,
    no_of_steps_per_rev_2TS=36,
    mesh_size=2e-3,
    magnet_mesh_size=1e-3,
    airgap_mesh_radial_div=5,
    airgap_mesh_circum_div=720,
    mesh_air_region_scale=1.15,
    only_table_results=False,
    csv_results=(r"Torque;Force;FEMCoilFlux;LineCurrent;TerminalVoltage;JouleLoss;TotalDisplacementAngle;"
                "JouleLoss_IronLoss;IronLoss_IronLoss;HysteresisLoss_IronLoss"),
    del_results_after_calc=False,
    run_folder=os.path.abspath("") + "/run_data/",
    jmag_csv_folder=os.path.abspath("") + "/run_data/JMAG_csv/",
    max_nonlinear_iterations=50,
    multiple_cpus=True,
    num_cpus=4,
    jmag_scheduler=False,
    jmag_visible=True,
)

problem = bmc.BSPMMachineConstantProblem(bp4,bp4_op_pt)
analyzer = bmc.BSPMMachineConstantAnalyzer(jmag_config)
analyzer.analyze(problem)
print(analyzer.Kt)
print(analyzer.Kf)
print(analyzer.Kdelta)
print(analyzer.Kphi)







