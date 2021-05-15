import sys

sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

stator1 = CrossSectOuterRotorStator(
    name='stator1',
    dim_alpha_st=DimDegree(30),
    dim_alpha_so=DimDegree((30 / 2) * 0.25),
    dim_r_si=DimMillimeter(15),
    dim_d_sy=DimMillimeter(7.5),
    dim_d_st=DimMillimeter(7.5),
    dim_d_sp=DimMillimeter(5),
    dim_d_so=DimMillimeter(3),
    dim_w_st=DimMillimeter(7.5),
    dim_r_st=DimMillimeter(0),
    dim_r_sb=DimMillimeter(0),
    dim_Q=8,
    location=mo.location2D()
)

toolMn = mn.MagNet(visible=True)
toolMn.open()

c1 = stator1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of Outer Rotor Stator
toolMn.prepare_section(c1)
