# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:54:12 2020

@author: Bharat
"""
import ToolBaseClasses as tbc
# create an instance of the MagNet class
MN = tbc.MagNet()
MN.open(iVisible = True)

# passing incorrect argument to drawLine to show error handling
l2 = MN.drawLine(1,2)

# set coordinated to draw line and arc
center = [0, 0]
start = [-11.5, 0]
end = [11.5,0]

# draw line and arc
l1 = MN.drawLine(start,end)
arc1 = MN.drawArc(center,start,end)

# select section which contains the coordinates provided
innerCoord = [0, -5]
MN.prepareSection(innerCoord)
# set properties of the material to be extruded
name1 = ["conductor"]
material1 = "Copper: 100% IACS"
depth1 = 10

# extrude section, comment out revolve if you want to see extrude in action
# extrude1 = MN.extrude(name1,material1,depth1)

# set properties of the material to be revolved
center1 = [0, 0]
axis1 = [1, 0]
angle1 = 90

#revlove section, comment out extrude if you want to see revolve in action
revolve1 = MN.revolve(name1, material1, center1, axis1, angle1)