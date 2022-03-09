import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn
import mach_cad.model_obj as mo


stator1 = mo.CrossSectOuterRotorStator(
    name="stator1",
    dim_alpha_st=mo.DimDegree(30),
    dim_alpha_so=mo.DimDegree((30 / 2) * 0.25),
    dim_r_si=mo.DimMillimeter(15),
    dim_d_sy=mo.DimMillimeter(7.5),
    dim_d_st=mo.DimMillimeter(7.5),
    dim_d_sp=mo.DimMillimeter(5),
    dim_d_so=mo.DimMillimeter(3),
    dim_w_st=mo.DimMillimeter(7.5),
    dim_r_st=mo.DimMillimeter(0),
    dim_r_sf=mo.DimMillimeter(0),
    dim_r_sb=mo.DimMillimeter(0),
    dim_Q=8,
    location=mo.Location2D(),
)

toolMn = mn.MagNet(visible=True)
toolMn.open()

c1 = stator1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of Outer Rotor Stator
toolMn.prepare_section(c1)
