# add the directory immediately above this file's directory to path for module import
import sys
sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)
z = mo.DimMillimeter(40)

# create hollowrectangle crossection object
hollow_rect = mo.CrossSectHollowRect(name = 'hollowRect1',location = mo.Location2D(),
                                     dim_t1 = x, dim_t2 = x, dim_t3 = x, dim_t4 = x,
                                     dim_w = y, dim_h = z)




# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw hollowrectangle
c1 = hollow_rect.draw(toolMn)

toolMn.view_all()
# select inner coordinate of a hollowrectangle
toolMn.prepare_section(c1) 

