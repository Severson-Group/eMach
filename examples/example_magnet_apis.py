# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 02:35:48 2020

@author: Bharat
"""

import emach.tools.magnet as mn

# create an instance of the MagNet class
MN = mn.MagNet()
MN.open(visible=True)


# draw circles with x,y as the coordinates of the centre, r as the radius
mn.document.view.draw_circle(MN.view, 0, 0, 20)
mn.document.view.draw_circle(MN.view, 0, 0, 30)
mn.document.view.draw_circle(MN.view, 0, 0, 50)

# select section
mn.document.view.select_section(MN.view, MN.consts, -1, 0)
# assign parameters needed for extrusion
section1 = ["conductor"]
material = "Copper: 100% IACS"
sweep_dist = 10
# extrude selected section by the distance specified in sweepDist with
# material and section name as provided.
sweep1Status = mn.document.view.make_component_in_a_line(
    MN.view, MN.consts, sweep_dist, section1, material
)

mn.document.view.select_section(MN.view, MN.consts, -25, 0)
section2 = ["air"]
material = "AIR"
# extrude selected section by the distance specified in sweepDist with
#material and section name as provided
sweep2Status = mn.document.view.make_component_in_a_line(
    MN.view, MN.consts, sweep_dist, section2, material
)

mn.document.view.select_section(MN.view, MN.consts, -35, 0)
section3 = ["iron"]
material = "Arnon 5"
# extrude selected section by the distance specified in sweepDist with
#material and section name as provided
sweep3Status = mn.document.view.make_component_in_a_line(
    MN.view, MN.consts, sweep_dist, section3, material
)

mat = mn.document.get_parameter(MN.disp_ex,
                                         section3[0], "Material")

# make a simple coil
coil1 = mn.document.make_simple_coil(MN.doc, 1, section1)

# assign relevant parameters to excite the coil
i_dc = 10
mn.document.set_parameter(MN.doc, coil1, "WaveFormType", "DC", MN.consts)
mn.document.set_parameter(MN.doc, coil1, "Current", i_dc, MN.consts)

curr = mn.document.get_parameter(MN.disp_ex, coil1, "Current")

"""
sin_offset = 0
sin_mag = 10
ArrayValues = [sin_offset, sin_mag]
MagnetFunc.setParameter(Doc,  coil1, "WaveFormType", "SIN", MNConsts)
MagnetFunc.setParameter(Doc,  coil1, "WaveFormValues", ArrayValues, MNConsts)
"""

# make a motion component
motion = mn.document.make_motion_component(MN.doc, section3)

# assign relevant parameters for the motion component
position_at_startup = 0
speed_at_startup = 0
time_array = 0
speed_array = 1000
time_speed = [time_array, speed_array]
direction = [0, 0, -1]
# set parameters for the motion component
mn.document.set_parameter(MN.doc, motion, "MotionSourceType",
                "VelocityDriven", MN.consts)
mn.document.set_parameter(MN.doc, motion, "MotionType", "Rotary", MN.consts)
mn.document.set_parameter(MN.doc, motion, "PositionAtStartup",
                position_at_startup, MN.consts)
mn.document.set_parameter(MN.doc, motion, "SpeedAtStartup", speed_at_startup, MN.consts)
mn.document.set_parameter(MN.doc, motion, "MotionDirection", direction, MN.consts)
mn.document.set_parameter(MN.doc, motion, "SpeedVsTime", time_speed, MN.consts)
