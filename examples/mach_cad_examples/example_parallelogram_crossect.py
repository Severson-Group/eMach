import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn
import mach_cad.model_obj as mo

x = mo.DimMillimeter(40)
y = mo.DimMillimeter(8)
z = mo.DimDegree(45)

# create parallelogram cross-section object
parallelogram1 = mo.CrossSectParallelogram(
    name="parallelogram1", location=mo.Location2D(), dim_l=x, dim_t=y, dim_theta=z
)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

c1 = parallelogram1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of parallelogram
toolMn.prepare_section(c1)
