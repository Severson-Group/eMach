# add the directory immediately above this file's directory to path for module import
import sys
sys.path.append("..")
import numpy as np

import emach.tools.magnet as mn
import emach.model_obj as mo

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)
z = mo.DimMillimeter(40)

# create hollowcylinder crossection object
hollowCylinder1 = mo.CrossSectHollowCylinder(name = 'hollowCylinder1',
                                                location = mo.Location2D(),
                                                dim_t = x, dim_r_o = y)

# create hollowcylinder component
comp1 = mo.Component(name = 'comp1', cross_sections = [hollowCylinder1],
                     material = mo.MaterialGeneric(name ='pm'),
                     make_solid = mo.MakeExtrude(location = mo.Location3D(), dim_depth = x))

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

comp1.make(toolMn,toolMn)
toolMn.view_all()

