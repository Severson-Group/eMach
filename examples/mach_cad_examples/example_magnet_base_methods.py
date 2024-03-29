import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_cad.tools.magnet as mn

# create an instance of the MagNet class
MN = mn.MagNet(visible=True)
MN.open()

# passing incorrect argument to drawLine to show error handling
# l2 = MN.drawLine('e1','2y')

# set default dimension to millimeter
MN.set_default_length("DimMillimeter", False)

# set coordinates to draw line and arc
center = [0, 0]
start = [-11.5, 0]
end = [11.5, 0]

# draw line and arc
l1 = MN.draw_line(start, end)
arc1 = MN.draw_arc(center, start, end)

# select section which contains the coordinates provided
# create dummy class to replicate CSToken
class DummyToken:
    pass


dt = DummyToken()
inner_coord = [0, -5]

setattr(dt, "inner_coord", inner_coord)
MN.prepare_section(dt)

# set properties of the material to be extruded
name1 = ["conductor"]
material1 = "Copper: 100% IACS"
depth1 = 10

# extrude section, comment out revolve if you want to see extrude in action
extrude1 = MN.extrude(name1, material1, depth1)

# set properties of the material to be revolved
center1 = [0, 0]
axis1 = [1, 0]
angle1 = 90

# revlove section, comment out extrude if you want to see revolve in action
# revolve1 = MN.revolve(name1, material1, center1, axis1, angle1)
del MN
