import sys

sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

x = mo.DimMillimeter(20)
y = mo.DimMillimeter(80)

# create solidrectange crossection object
solid_rect = mo.CrossSectSolidRectangle(name='solidRect1', location=mo.Location2D(),
                                        dim_w=x, dim_h=y)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw solid rectangle
c1 = solid_rect.draw(toolMn)

toolMn.view_all()
# select inner coordinate of a solid rectangle
toolMn.prepare_section(c1)
