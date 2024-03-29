import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn
import mach_cad.model_obj as mo

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)
z = mo.DimMillimeter(40)

# create CrossSectInnerNotchedRotor object
innerNotchedRotor1 = mo.CrossSectInnerNotchedRotor(
    name="rotor",
    location=mo.Location2D(),
    dim_alpha_rm=mo.DimDegree(60),
    dim_alpha_rs=mo.DimDegree(10),
    dim_d_ri=mo.DimMillimeter(8),
    dim_r_ri=mo.DimMillimeter(40),
    dim_d_rp=mo.DimMillimeter(5),
    dim_d_rs=mo.DimMillimeter(3),
    p=2,
    s=4,
)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw inner notched rotor
c1 = innerNotchedRotor1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of cross-section
toolMn.prepare_section(c1)
