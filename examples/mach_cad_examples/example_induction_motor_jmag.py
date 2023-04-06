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
stator_partial = mo.CrossSectInnerRotorStatorPartial(
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

winding_layer1 = mo.CrossSectInnerRotorStatorRightSlot(
    name="WindingLayer1",
    stator_core=stator_partial,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(0)),
    )

winding_layer2 = mo.CrossSectInnerRotorStatorLeftSlot(
    name="WindingLayer2",
    stator_core=stator_partial,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(0)),
    )

rotor_partial = mo.CrossSectInnerRotorDropSlotsPartial(
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

bar = mo.CrossSectInnerRotorDropSlotsBar(
    name="Bar",
    rotor_core=rotor_partial,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(0)),
    theta=mo.DimDegree(0),
    )

###################### Draw the motor in JMAG ######################
tool_jmag = JMAG.JmagDesigner()

# Check if a specified file name exists already
file = r"example_induction_motor.jproj"
attempts = 1
if os.path.exists(file):
    print(
        "JMAG project exists already, I will not delete it but create a new one with a different name instead."
    )
    attempts = 2
    temp_path = file[
        : -len(".jproj")
    ] + "_attempts_%d.jproj" % (attempts)
    while os.path.exists(temp_path):
        attempts += 1
        temp_path = file[
            : -len(".jproj")
        ] + "_attempts_%d.jproj" % (attempts)

    file = temp_path

tool_jmag.open(comp_filepath=file, length_unit="DimMillimeter", study_type="Transient")
tool_jmag.set_visibility(True)

# Draw the model
tool_jmag.sketch = tool_jmag.create_sketch()
tool_jmag.sketch.SetProperty("Name", stator_partial.name)
tool_jmag.sketch.SetProperty("Color", r"#808080")
cs_stator = stator_partial.draw(tool_jmag)
stator_tool = tool_jmag.prepare_section(cs_stator, num_copy_rotate=Q)

tool_jmag.sketch = tool_jmag.create_sketch()
tool_jmag.sketch.SetProperty("Name", winding_layer1.name)
tool_jmag.sketch.SetProperty("Color", r"#B87333")
cs_winding_layer1 = winding_layer1.draw(tool_jmag)
winding_tool1 = tool_jmag.prepare_section(cs_winding_layer1, num_copy_rotate=Q)

tool_jmag.sketch = tool_jmag.create_sketch()
tool_jmag.sketch.SetProperty("Name", winding_layer2.name)
tool_jmag.sketch.SetProperty("Color", r"#B87333")
cs_winding_layer2 = winding_layer2.draw(tool_jmag)
winding_tool2 = tool_jmag.prepare_section(cs_winding_layer2, num_copy_rotate=Q)

tool_jmag.sketch = tool_jmag.create_sketch()
tool_jmag.sketch.SetProperty("Name", rotor_partial.name)
tool_jmag.sketch.SetProperty("Color", r"#808080")
cs_rotor_core = rotor_partial.draw(tool_jmag)
rotor_tool = tool_jmag.prepare_section(cs_rotor_core, num_copy_rotate=Qr)

tool_jmag.sketch = tool_jmag.create_sketch()
tool_jmag.sketch.SetProperty("Name", bar.name)
tool_jmag.sketch.SetProperty("Color", r"#C89E9B")
cs_rotor_bar = bar.draw(tool_jmag)
rotor_bar_tool = tool_jmag.prepare_section(cs_rotor_bar, num_copy_rotate=Qr)

tool_jmag.doc.SaveModel(False)

# Save the file
tool_jmag.save()
