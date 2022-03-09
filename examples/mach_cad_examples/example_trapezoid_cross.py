import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn
import mach_cad.model_obj as mo
import numpy as np

x = mo.DimMillimeter(40)
y = mo.DimMillimeter(80)
z = mo.DimDegree(60)

# create trapezoid cross-section object
trapezoid1 = mo.CrossSectTrapezoid(
    name="trapezoid1", location=mo.Location2D(), dim_h=x, dim_w=y, dim_theta=z
)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

c1 = trapezoid1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of trapezoid
toolMn.prepare_section(c1)
