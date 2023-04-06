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
from mach_eval.machines.materials.electric_steels import M19Gauge29
from mach_eval.machines.materials.miscellaneous_materials import (
    Steel,
    Copper,
    Hub,
    Air,
)

# Motor dimensions
stator_dimensions = {
    'alpha_st': 50,
    'alpha_so': 22.25,
    'r_si': 14.16,
    'd_so': 2.71,
    'd_sp': 4.07,
    'd_st': 11.27,
    'd_sy': 9,
    'w_st': 9.09,
    'alpha_m': 178.78,
    'l_st': 1,
}

rotor_dimensions = {
    'r_ri': 3,
    'd_ri': 4,
    'd_rb': 2,
    'r_rb1': 1,
    'r_rb2': 0.5,
    'd_so': 2,
    'w_so': 0.5,
}

# Number of stator and rotor slots
Q = 6
Qr = 12

# Boundary parameters (for FEMM)
radius_boundary = 100
radius_air_region1 = 13.6
radius_air_region2 = 70

# Materials
Aluminium = {
    "bar_material": "Aluminium"
}

bim_materials = {
    "air_mat": Air,
    "rotor_iron_mat": M19Gauge29,
    "stator_iron_mat": M19Gauge29,
    "coil_mat": Copper,
    "rotor_bar_mat": Aluminium,
    "shaft_mat": Steel,
    "rotor_hub": Hub,
}


###################### Create cross-section objects ######################
stator = mo.CrossSectInnerRotorStator(
    name="StatorCore",
    dim_alpha_st=mo.DimDegree(stator_dimensions["alpha_st"]),
    dim_alpha_so=mo.DimDegree(stator_dimensions["alpha_so"]),
    dim_r_si=mo.DimMillimeter(stator_dimensions["r_si"]),
    dim_d_so=mo.DimMillimeter(stator_dimensions["d_so"]),
    dim_d_sp=mo.DimMillimeter(stator_dimensions["d_sp"]),
    dim_d_st=mo.DimMillimeter(stator_dimensions["d_st"]),
    dim_d_sy=mo.DimMillimeter(stator_dimensions["d_sy"]),
    dim_w_st=mo.DimMillimeter(stator_dimensions["w_st"]),
    dim_r_st=mo.DimMillimeter(0),
    dim_r_sf=mo.DimMillimeter(0),
    dim_r_sb=mo.DimMillimeter(0),
    Q=Q,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(0)),
    theta=mo.DimDegree(0),
)

winding_layer1 = []
for i in range (0, Q):
    winding_layer1.append(mo.CrossSectInnerRotorStatorRightSlot(
        name="WindingLayer1",
        stator_core=stator,
        location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(2 * np.pi / Q * i)),
        ))

winding_layer2 = []
for i in range (0, Q):
    winding_layer2.append(mo.CrossSectInnerRotorStatorLeftSlot(
        name="WindingLayer2",
        stator_core=stator,
        location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(2 * np.pi / Q * i)),
        theta=mo.DimDegree(0),
        ))

rotor = mo.CrossSectInnerRotorDropSlots(
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

bar = []
for i in range(0,Qr):
    bar.append(mo.CrossSectInnerRotorDropSlotsBar(
    name="Bar",
    rotor_core=rotor,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(2 * np.pi / Qr * i)),
    theta=mo.DimDegree(0),
    ))

###################### Create component objects ######################
comp_stator = mo.Component(
        name="StatorCore",
        cross_sections=[stator],
        material=mo.MaterialGeneric(name=bim_materials["stator_iron_mat"]["core_material"]),
        make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(stator_dimensions["l_st"])),
        )

comp_winding_layer1 = []
for i in range(0,Q):
    comp_winding_layer1.append(mo.Component(
        name="WindingLayer1",
        cross_sections=[winding_layer1[i]],
        material=mo.MaterialGeneric(name="Copper", color=r"#4d4b4f"),
        make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(stator_dimensions["l_st"])),
        ))

comp_winding_layer2 = []
for i in range(0,Q):
    comp_winding_layer2.append(mo.Component(
        name="WindingLayer2",
        cross_sections=[winding_layer2[i]],
        material=mo.MaterialGeneric(name="Copper", color=r"#4d4b4f"),
        make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(stator_dimensions["l_st"])),
        ))

comp_rotor = mo.Component(
    name="RotorCore",
    cross_sections=[rotor],
    material=mo.MaterialGeneric(name=bim_materials["rotor_iron_mat"]["core_material"]),
    make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(stator_dimensions["l_st"])),
    )

comp_bar = []
for i in range(0,Qr):
    comp_bar.append(mo.Component(
    name="Bar",
    cross_sections=[bar[i]],
    material=mo.MaterialGeneric(name="Copper", color=r"#4d4b4f"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(1)),
    ))

###################### Draw the motor in FEMM ######################
tool_femm = FEMM.FEMMDesigner()
tool_femm.newdocument(1, 0)
tool_femm.probdef(0, 'millimeters', 'planar', 1e-8, 1, 30, 1)
# Add materials
tool_femm.add_material("Air")
tool_femm.add_material("Copper")
tool_femm.add_new_material(mat_name=bim_materials["rotor_bar_mat"]["bar_material"])
hdata, bdata = np.loadtxt(bim_materials["stator_iron_mat"]['core_bh_file'], unpack=True, usecols=(0, 1))
tool_femm.add_new_material(mat_name=bim_materials["stator_iron_mat"]["core_material"],hdata=hdata,bdata=bdata)

# Draw the model
stator_tool = comp_stator.make(tool_femm, tool_femm)
winding_tool1 = []
for i in range(0,Q):
    winding_tool1.append(comp_winding_layer1[i].make(tool_femm, tool_femm))
winding_tool2 = []
for i in range(0,Q):
    winding_tool2.append(comp_winding_layer2[i].make(tool_femm, tool_femm))
rotor_tool = comp_rotor.make(tool_femm, tool_femm)
bar_tool = []
for i in range(0,Qr):
    bar_tool.append(comp_bar[i].make(tool_femm, tool_femm))

# Assign 'Air' material
tool_femm.set_block_prop(
    new_block=1,
    inner_coord=[0, 0],
    material_name='Air',
    )
tool_femm.set_block_prop(
    new_block=1,
    inner_coord=[radius_air_region1, 0],
    material_name='Air',
    )
tool_femm.set_block_prop(
    new_block=1,
    inner_coord=[radius_air_region2, 0],
    material_name='Air',
    )

# Create boundary condition
tool_femm.create_boundary_condition(number_of_shells=7, radius=radius_boundary, centerxy=(0,0), bc=1)

# Check if a specified file name exists already
file = r"example_induction_motor.fem"
attempts = 1
if os.path.exists(file):
    print(
        "FEMM project exists already, I will not delete it but create a new one with a different name instead."
    )
    attempts = 2
    temp_path = file[
        : -len(".fem")
    ] + "_attempts_%d.fem" % (attempts)
    while os.path.exists(temp_path):
        attempts += 1
        temp_path = file[
            : -len(".fem")
        ] + "_attempts_%d.fem" % (attempts)

    file = temp_path

# Save the file
tool_femm.save_as(file)
