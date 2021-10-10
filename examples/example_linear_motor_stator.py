# add the directory immediately above this file's directory to path for module import
import sys

sys.path.append("..")

import emach.tools.magnet as mn
import emach.model_obj as mo
import numpy as np

# Stator parameters
w_s = 65.7  # stator length
w_st = 14.8  # tooth thickness
w_so = 3.66  # slot opening length
r_so = 71.8  # stator outer radius
r_si = 35.9  # stator inner radius
d_so = 2  # slot opening height
d_sp = 4  # height of tooth end
d_sy = 9.53  # stator yoke thickness
d_st = r_so - r_si - d_sy - d_sp
w_ss = (w_s - 2 * w_st) / 2
# radii of fillets
r_st = 3
r_sf = 3
r_sb = 3

# create linear stator crossection object

stator_iron = mo.CrossSectLinearMotorStator(name='stator_iron',
                                            location=mo.Location2D(),
                                            dim_w_s=mo.DimMillimeter(w_s),
                                            dim_w_st=mo.DimMillimeter(w_st),
                                            dim_w_so=mo.DimMillimeter(w_so),
                                            dim_r_so=mo.DimMillimeter(r_so),
                                            dim_r_si=mo.DimMillimeter(r_si),
                                            dim_d_so=mo.DimMillimeter(d_so),
                                            dim_d_sp=mo.DimMillimeter(d_sp),
                                            dim_d_sy=mo.DimMillimeter(d_sy),
                                            dim_r_st=mo.DimMillimeter(r_st),
                                            dim_r_sf=mo.DimMillimeter(r_sf),
                                            dim_r_sb=mo.DimMillimeter(r_sb))

# create an instance of the MagNet class
toolMn = mn.MagNet(visible=True)
toolMn.open()

# draw linear stator
c1 = stator_iron.draw(toolMn)

toolMn.view_all()
# select inner coordinate of a hollow cylinder
toolMn.prepare_section(c1)
