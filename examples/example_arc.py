# add the directory immediately above this file's directory to path for module import
import sys
sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)
z = mo.DimDegree(40)

# create arc crossection object
arc1 = mo.CrossSectArc(name = 'arc1',location = mo.Location2D(),\
                       dim_d_a = x, dim_r_o = y, dim_alpha = z)



# create another arc crossection
arc2 = mo.CrossSectArc(name = 'arc2',location = mo.Location2D(),\
                        dim_d_a = x*2, dim_r_o = y/2, dim_alpha = z*3)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw arcs
c1 = arc1.draw(toolMn)
c2 = arc2.draw(toolMn)

toolMn.view_all()
# select inner coordinate of an arc
toolMn.prepare_section(c2)

