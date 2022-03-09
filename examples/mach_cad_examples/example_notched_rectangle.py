import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn
import mach_cad.model_obj as mo

w = mo.DimMillimeter(100)
w_n = mo.DimMillimeter(15)
d = mo.DimMillimeter(20)
d_n = mo.DimMillimeter(10)

# create Notched Rectangle crossection object
notchedRectangle1 = mo.CrossSectNotchedRectangle(
    name="notchedRectangle1",
    location=mo.Location2D(),
    dim_w=w,
    dim_w_n=w_n,
    dim_d=d,
    dim_d_n=d_n,
)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw Notched rectangle
c1 = notchedRectangle1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of a Notched rectangle
toolMn.prepare_section(c1)
