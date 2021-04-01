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
hollowCylinder1 = mo.CrossSectHollowCylinder(name = 'hollowCylinder1',
                                                location = mo.Location2D(),
                                                dim_t = x, dim_r_o = y)



# create clone of hollowcylinder crossection
hollowCylinder2 = hollowCylinder1.clone(name = 'hollowCylinder2', 
                                        location = mo.Location2D(anchor_xy = \
                                        np.array([mo.DimMillimeter(-70), mo.DimMillimeter(100)])),
                                        dim_r_o = z)

# create an instance of the MagNet class
toolMn = mn.MagNet()
toolMn.open(visible=True)

# draw hollowcylinders
c1 = hollowCylinder1.draw(toolMn)
c2 = hollowCylinder2.draw(toolMn)

toolMn.view_all()
# select inner coordinate of a hollow cylinder
toolMn.prepare_section(c2.inner_coord)