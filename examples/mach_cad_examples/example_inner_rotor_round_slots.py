import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.jmag as JMAG
from mach_cad.tools.femm import FEMM
import mach_cad.model_obj as mo
import numpy as np
from mach_eval.machines.materials.electric_steels import M19Gauge29

# rotor dimensions
rotor_dimensions = {
    'r_ri': 3,
    'd_ri': 4,
    'r_rb': 1,
    'd_so': 2,
    'w_so': 0.5,
}

# create cross-section 
rotor1 = mo.CrossSectInnerRotorRoundSlots(
    name="RotorCore",
    dim_r_ri=mo.DimMillimeter(rotor_dimensions["r_ri"]),
    dim_d_ri=mo.DimMillimeter(rotor_dimensions["d_ri"]),
    dim_r_rb=mo.DimMillimeter(rotor_dimensions["r_rb"]),
    dim_d_so=mo.DimMillimeter(rotor_dimensions["d_so"]),
    dim_w_so=mo.DimMillimeter(rotor_dimensions["w_so"]),
    Qr=12,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
    theta=mo.DimDegree(0),
)

# create component
comp1 = mo.Component(
    name="RotorCore",
    cross_sections=[rotor1],
    material=mo.MaterialGeneric(name=M19Gauge29["core_material"]),
    make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(1)),
)


# create an instance of the FEMM class
toolFEMM = FEMM.FEMMDesigner()
toolFEMM.newdocument(hide_window=1, problem_type=0)
toolFEMM.probdef()
# Add a new material and its BH curve to the FEMM project
hdata, bdata = np.loadtxt(M19Gauge29['core_bh_file'], unpack=True, usecols=(0, 1))
toolFEMM.add_new_material(mat_name=M19Gauge29["core_material"],hdata=hdata,bdata=bdata)
rotor_tool = comp1.make(toolFEMM, toolFEMM)
toolFEMM.save_as("inner_rotor_round_slots.fem")


# create an instance of the JMAG class
toolJMAG = JMAG.JmagDesigner()
file = r"inner_rotor_round_slots.jproj"
toolJMAG.open(comp_filepath=file, study_type="Transient")
toolJMAG.set_visibility(True)
rotor_tool = comp1.make(toolJMAG, toolJMAG)
toolJMAG.save()