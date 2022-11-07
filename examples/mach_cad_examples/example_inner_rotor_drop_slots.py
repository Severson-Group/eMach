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
    'd_rb': 2,
    'r_rb1': 1,
    'r_rb2': 0.5,
    'd_so': 2,
    'w_so': 0.5,
}

Qr = 12

# create cross-section 
rotor1 = mo.CrossSectInnerRotorDropSlots(
    name="RotorCore",
    dim_r_ri=mo.DimMillimeter(rotor_dimensions["r_ri"]),
    dim_d_ri=mo.DimMillimeter(rotor_dimensions["d_ri"]),
    dim_d_rb=mo.DimMillimeter(rotor_dimensions["d_rb"]),
    dim_r_rb1=mo.DimMillimeter(rotor_dimensions["r_rb1"]),
    dim_r_rb2=mo.DimMillimeter(rotor_dimensions["r_rb2"]),
    dim_d_so=mo.DimMillimeter(rotor_dimensions["d_so"]),
    dim_w_so=mo.DimMillimeter(rotor_dimensions["w_so"]),
    Qr=Qr,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
    theta=mo.DimDegree(0),
)

bar1 = []
for i in range(0,Qr):
    bar1.append(mo.CrossSectInnerRotorDropSlotsBar(
    name="Bar1",
    rotor_core=rotor1,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(2 * np.pi / Qr * i)),
    theta=mo.DimDegree(0),
    ))

# create component
comp1 = mo.Component(
    name="RotorCore",
    cross_sections=[rotor1],
    material=mo.MaterialGeneric(name=M19Gauge29["core_material"]),
    make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(1)),
)

comp2 = []
for i in range(0,Qr):
    comp2.append(mo.Component(
    name="Bar1",
    cross_sections=[bar1[i]],
    material=mo.MaterialGeneric(name="Copper", color=r"#4d4b4f"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(1)),
    ))


# create an instance of the FEMM class
toolFEMM = FEMM.FEMMDesigner()
toolFEMM.newdocument(hide_window=1, problem_type=0)
toolFEMM.probdef()
toolFEMM.add_material("Copper")
# Add a new material and its BH curve to the FEMM project
hdata, bdata = np.loadtxt(M19Gauge29['core_bh_file'], unpack=True, usecols=(0, 1))
toolFEMM.add_new_material(mat_name=M19Gauge29["core_material"],hdata=hdata,bdata=bdata)
rotor_tool = comp1.make(toolFEMM, toolFEMM)
bar_tool = []
for i in range(0,Qr):
    bar_tool.append(comp2[i].make(toolFEMM, toolFEMM))
toolFEMM.save_as("inner_rotor_drop_slots.fem")


# create an instance of the JMAG class
toolJMAG = JMAG.JmagDesigner()
file = r"inner_rotor_drop_slots.jproj"
toolJMAG.open(comp_filepath=file, study_type="Transient")
toolJMAG.set_visibility(True)
rotor_tool = comp1.make(toolJMAG, toolJMAG)
bar_tool = []
for i in range(0,Qr):
    bar_tool.append(comp2[i].make(toolJMAG, toolJMAG))
toolJMAG.save()