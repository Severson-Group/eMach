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
    'd_rb': 1,
    'r_rb': 1,
    'd_so': 2,
    'w_so': 0.5,
}

Qr = 12

###################### Create cross-section objects ######################
# Partial models are used in JMAG (to reduce drawing time)

rotor = mo.CrossSectInnerRotorRoundSlotsDoubleCage(
    name="RotorCore",
    dim_r_ri=mo.DimMillimeter(rotor_dimensions["r_ri"]),
    dim_d_ri=mo.DimMillimeter(rotor_dimensions["d_ri"]),
    dim_d_rb=mo.DimMillimeter(rotor_dimensions["d_rb"]),
    dim_r_rb=mo.DimMillimeter(rotor_dimensions["r_rb"]),
    dim_d_so=mo.DimMillimeter(rotor_dimensions["d_so"]),
    dim_w_so=mo.DimMillimeter(rotor_dimensions["w_so"]),
    Qr=12,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
    theta=mo.DimDegree(0),
)

rotor_partial = mo.CrossSectInnerRotorRoundSlotsDoubleCagePartial(
    name="RotorCore",
    dim_r_ri=mo.DimMillimeter(rotor_dimensions["r_ri"]),
    dim_d_ri=mo.DimMillimeter(rotor_dimensions["d_ri"]),
    dim_d_rb=mo.DimMillimeter(rotor_dimensions["d_rb"]),
    dim_r_rb=mo.DimMillimeter(rotor_dimensions["r_rb"]),
    dim_d_so=mo.DimMillimeter(rotor_dimensions["d_so"]),
    dim_w_so=mo.DimMillimeter(rotor_dimensions["w_so"]),
    Qr=12,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)]),
    theta=mo.DimDegree(0),
)

bar1 = []
for i in range(0,Qr):
    bar1.append(mo.CrossSectInnerRotorRoundSlotsDoubleCageBar1(
    name="Bar1",
    rotor_core=rotor,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(2 * np.pi / Qr * i)),
    theta=mo.DimDegree(0),
    ))

bar1_partial = bar1[0]

bar2 = []
for i in range(0,Qr):
    bar2.append(mo.CrossSectInnerRotorRoundSlotsDoubleCageBar2(
    name="Bar2",
    rotor_core=rotor,
    location=mo.Location2D(anchor_xy=[mo.DimMillimeter(0), mo.DimMillimeter(0)],theta=mo.DimRadian(2 * np.pi / Qr * i)),
    theta=mo.DimDegree(0),
    ))

bar2_partial = bar2[0]


###################### Create component objects ######################
# Only used in FEMM. Can also be used in JMAG, but increases drawing time.

comp_rotor = mo.Component(
    name="RotorCore",
    cross_sections=[rotor],
    material=mo.MaterialGeneric(name=M19Gauge29["core_material"]),
    make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(1)),
)

comp_bar1 = []
for i in range(0,Qr):
    comp_bar1.append(mo.Component(
    name="Bar1",
    cross_sections=[bar1[i]],
    material=mo.MaterialGeneric(name="Copper", color=r"#4d4b4f"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(1)),
    ))

comp_bar2 = []
for i in range(0,Qr):
    comp_bar2.append(mo.Component(
    name="Bar2",
    cross_sections=[bar2[i]],
    material=mo.MaterialGeneric(name="Copper", color=r"#4d4b4f"),
    make_solid=mo.MakeExtrude(location=mo.Location3D(), dim_depth=mo.DimMillimeter(1)),
    ))


###################### Draw the motor in FEMM ######################
tool_femm = FEMM.FEMMDesigner()
tool_femm.newdocument(hide_window=1, problem_type=0)
tool_femm.probdef()
tool_femm.add_material("Copper")
# Add a new material and its BH curve to the FEMM project
hdata, bdata = np.loadtxt(M19Gauge29['core_bh_file'], unpack=True, usecols=(0, 1))
tool_femm.add_new_material(mat_name=M19Gauge29["core_material"],hdata=hdata,bdata=bdata)
rotor_tool = comp_rotor.make(tool_femm, tool_femm)
bar1_tool = []
for i in range(0,Qr):
    bar1_tool.append(comp_bar1[i].make(tool_femm, tool_femm))
bar2_tool = []
for i in range(0,Qr):
    bar2_tool.append(comp_bar2[i].make(tool_femm, tool_femm))

# Check if a specified file name exists already
file = r"inner_rotor_round_slots_double_cage.fem"
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


###################### Draw the motor in JMAG ######################
tool_jmag = JMAG.JmagDesigner()
file = r"inner_rotor_round_slots_double_cage.jproj"
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
tool_jmag.sketch.SetProperty("Name", rotor_partial.name)
tool_jmag.sketch.SetProperty("Color", r"#808080")
cs_rotor_core = rotor_partial.draw(tool_jmag)
rotor_tool = tool_jmag.prepare_section(cs_rotor_core, num_copy_rotate=Qr)

tool_jmag.sketch = tool_jmag.create_sketch()
tool_jmag.sketch.SetProperty("Name", bar1_partial.name)
tool_jmag.sketch.SetProperty("Color", r"#C89E9B")
cs_rotor_bar1 = bar1_partial.draw(tool_jmag)
rotor_bar_tool1 = tool_jmag.prepare_section(cs_rotor_bar1, num_copy_rotate=Qr)

tool_jmag.sketch = tool_jmag.create_sketch()
tool_jmag.sketch.SetProperty("Name", bar2_partial.name)
tool_jmag.sketch.SetProperty("Color", r"#C89E9B")
cs_rotor_bar2 = bar2_partial.draw(tool_jmag)
rotor_bar_tool2 = tool_jmag.prepare_section(cs_rotor_bar2, num_copy_rotate=Qr)

tool_jmag.doc.SaveModel(False)

# Save the file
tool_jmag.save()
