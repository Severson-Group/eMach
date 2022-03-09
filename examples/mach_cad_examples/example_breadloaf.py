import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn
import mach_cad.model_obj as mo
import numpy as np

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)
z = mo.DimMillimeter(40)

# create breadloaf crossection object
breadloaf1 = mo.CrossSectBreadloaf(
    name="breadloaf1",
    location=mo.Location2D(),
    dim_w=z,
    dim_l=x,
    dim_r=y,
    dim_alpha=mo.DimDegree(70),
)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw breadloaf
c1 = breadloaf1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of brealoaf
toolMn.prepare_section(c1)
