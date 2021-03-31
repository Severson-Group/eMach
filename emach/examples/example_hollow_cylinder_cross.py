# add the directory immediately above this file's directory to path for module import
import sys
sys.path.append("..")

import tools.magnet as mn
import model_obj as mo
import numpy as np

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)
z = mo.DimMillimeter(40)

# create hollowcylinder crossection object
hollowCylinder1 = mo.cross_sects.CrossSectHollowCylinder(name = 'hollowCylinder1',
                                                location = mo.Location2D(),
                                                dim_t = x, dim_r_o = y)



# create clone of hollowcylinder crossection
hollowCylinder2 = hollowCylinder1.clone(name = 'hollowCylinder2', 
                                        location = mo.Location2D(anchor_xy = \
                                        np.array([mo.DimMillimeter(-70), mo.DimMillimeter(100)])),
                                        dim_r_o = z)


# create hollowcylinder component
comp1 = mo.Component(name = ['comp1'], cross_sections = [hollowCylinder1], \
                     material = mo.MaterialGeneric(name ='pm'), make_solid = mo.MakeExtrude(x))

# create an instance of the MagNet class
toolMn = mn.MagNet()
toolMn.open(visible=True)

comp1.make(toolMn,toolMn)
toolMn.view_all()