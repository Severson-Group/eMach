# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 01:02:08 2020

@author: Bharat
"""
import tools.magnet as mn
import model_obj as mo

hollowCylinder1 = mo.cross_sects.HollowCylinder(
    name="hollowCylinder1", dim_d_a=4, dim_r_o=80, location=mo.Location2D()
)

# create an instance of the MagNet class
toolMn = mn.MagNet()
toolMn.open(visible=True)

c1 = hollowCylinder1.draw(toolMn)

toolMn.view_all()
toolMn.prepare_section(c1.inner_coord)
