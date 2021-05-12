import sys

sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

x = mo.DimMillimeter(40)
y = mo.DimMillimeter(8)
z = mo.DimDegree(45)

# create parallelogram cross-section object
parallelogram1 = mo.CrossSectParallelogram(name='parallelogram1', location=mo.Location2D(),
                                   dim_l=x, dim_t=y, dim_theta=z)

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

c1 = parallelogram1.draw(toolMn)

toolMn.view_all()
# select inner coordinate of parallelogram
toolMn.prepare_section(c1)