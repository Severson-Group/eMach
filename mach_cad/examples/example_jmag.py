import sys

sys.path.append("..")

import emach.tools.jmag as jd
import emach.model_obj as mo

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)
z = mo.DimMillimeter(40)

# create breadloaf crossection object
breadloaf1 = mo.CrossSectBreadloaf(name='breadloaf1', location=mo.Location2D(),
                                   dim_w=z, dim_l=x, dim_r=y, dim_alpha=mo.DimDegree(70))

tool_jmag = jd.JmagDesigner()
file = r'one.jproj'
tool_jmag.open(filepath=file)

# draw breadloaf
c1 = breadloaf1.draw(tool_jmag)
