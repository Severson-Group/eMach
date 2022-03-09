import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn
import mach_cad.model_obj as mo

rotor1 = mo.CrossSectOuterRotor(
    name="rotor1",
    dim_alpha_rs=mo.DimDegree(20),
    dim_alpha_rm=mo.DimDegree(60),
    dim_r_ro=mo.DimMillimeter(30),
    dim_d_rp=mo.DimMillimeter(5),
    dim_d_ri=mo.DimMillimeter(5),
    dim_d_rs=mo.DimMillimeter(8),
    dim_p=2,
    dim_S=1,
    location=mo.Location2D(),
)

toolMn = mn.MagNet(visible=True)
toolMn.open()

c1 = rotor1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of Outer Rotor
toolMn.prepare_section(c1)
