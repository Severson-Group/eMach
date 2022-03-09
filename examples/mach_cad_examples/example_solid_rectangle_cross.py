import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn
import mach_cad.model_obj as mo

x = mo.DimMillimeter(20)
y = mo.DimMillimeter(80)

# create solidrectange crossection object
solid_rect = mo.CrossSectSolidRectangle(
    name="solidRect1", location=mo.Location2D(), dim_w=x, dim_h=y
)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw solid rectangle
c1 = solid_rect.draw(toolMn)

toolMn.view_all()
# select inner coordinate of a solid rectangle
toolMn.prepare_section(c1)
