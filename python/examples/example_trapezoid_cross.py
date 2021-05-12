import sys

sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

x = mo.DimMillimeter(40)
y = mo.DimMillimeter(80)
z = mo.DimDegree(60)

# create trapezoid cross-section object
trapezoid1 = mo.CrossSectTrapezoid(name='trapezoid1', location=mo.Location2D(),
                                   dim_h=x, dim_w=y, dim_theta=z)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

c1 = trapezoid1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of trapezoid
toolMn.prepare_section(c1)
