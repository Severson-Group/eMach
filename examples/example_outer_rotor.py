import sys

sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

rotor1 = CrossSectOuterRotor(
    name='rotor1',
    dim_alpha_rs=mo.DimDegree(20),
    dim_alpha_rm=mo.DimDegree(60),
    dim_R_ro=mo.DimMillimeter(30),
    dim_d_rp=mo.DimMillimeter(5),
    dim_d_ri=mo.DimMillimeter(5),
    dim_d_rs=mo.DimMillimeter(8),
    dim_P=2,
    dim_S=1,
    location=mo.Location2D()
)

toolMn = mn.MagNet(visible=True)
toolMn.open()

c1 = rotor1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of Outer Rotor
toolMn.prepare_section(c1)
