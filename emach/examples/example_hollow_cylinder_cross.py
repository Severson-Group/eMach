# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 01:02:08 2020

@author: Bharat
"""
# add the directory immediately above this file's directory to path for module import
import sys
sys.path.append("..")

import tools.magnet as mn
import model_obj as mo

x = mo.DimMillimeter(4)
y = mo.DimMillimeter(80)


hollowCylinder1 = mo.cross_sects.CrossSectHollowCylinder(name = 'hollowCylinder1',
                                                dim_d_a = x, dim_r_o = y,
                                                location = mo.Location2D())

# create an instance of the MagNet class
toolMn = mn.MagNet()
toolMn.open(visible=True)

c1 = hollowCylinder1.draw(toolMn)

toolMn.view_all()
toolMn.prepare_section(c1.inner_coord)