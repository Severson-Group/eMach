import sys

sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

w = mo.DimMillimeter(100)
w_n = mo.DimMillimeter(15)
d = mo.DimMillimeter(20)
d_n = mo.DimMillimeter(10)

# create Notched Rectangle crossection object
notchedRectangle1 = mo.CrossSectNotchedRectangle(name='notchedRectangle1', location=mo.Location2D(),
                                               dim_w=w, dim_w_n=w_n,
                                               dim_d=d, dim_d_n=d_n)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw Notched rectangle
c1 = notchedRectangle1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of a Notched rectangle
toolMn.prepare_section(c1)
