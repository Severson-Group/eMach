# add the directory immediately above this file's directory to path for module import
import sys
sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)
z = mo.DimMillimeter(40)


stator4 = mo.CrossSectInnerRotorStator( name = 'stator1', 
                                        dim_alpha_st = mo.DimDegree(40), 
                                        dim_alpha_so = mo.DimDegree(20), 
                                        dim_r_si = mo.DimMillimeter(40), 
                                        dim_d_so = mo.DimMillimeter(5), 
                                        dim_d_sp = mo.DimMillimeter(10), 
                                        dim_d_st = mo.DimMillimeter(15), 
                                        dim_d_sy = mo.DimMillimeter(15), 
                                        dim_w_st = mo.DimMillimeter(13), 
                                        dim_r_st = mo.DimMillimeter(0), 
                                        dim_r_sf = mo.DimMillimeter(0), 
                                        dim_r_sb = mo.DimMillimeter(0), 
                                        Q = 6,
                                        location = mo.Location2D())


# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw hollowcylinders
c1 = stator4.draw(toolMn)

toolMn.view_all()
# select inner coordinate of a hollow cylinder
toolMn.prepare_section(c1)

