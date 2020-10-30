# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 02:35:48 2020

@author: Bharat
"""
import emach as em

# create an instance of the MagNet class
mn = em.MagNet()
mn.open(i_visible=True)


# draw circles with x,y as the coordinates of the centre, r as the radius
em.draw_circle(mn.view, 0, 0, 20)
em.draw_circle(mn.view, 0, 0, 30)
em.draw_circle(mn.view, 0, 0, 50)

# select section
em.select_section(mn.view, mn.consts, -1, 0)
# assign parameters needed for extrusion
section1 = ["conductor"]
material = "Copper: 100% IACS"
sweep_dist = 10
# extrude selected section by the distance specified in sweepDist with
# material and section name as provided.
sweep1Status = em.make_component_in_a_line(
    mn.view, mn.consts, sweep_dist, section1, material
)

em.select_section(mn.view, mn.consts, -25, 0)
section2 = ["air"]
material = "AIR"
# extrude selected section by the distance specified in sweepDist with
#material and section name as provided
sweep2Status = em.make_component_in_a_line(
    mn.view, mn.consts, sweep_dist, section2, material
)

em.select_section(mn.view, mn.consts, -35, 0)
section3 = ["iron"]
material = "Arnon 5"
# extrude selected section by the distance specified in sweepDist with
#material and section name as provided
sweep3Status = em.make_component_in_a_line(
    mn.view, mn.consts, sweep_dist, section3, material
)

mat = em.tool_magnet.document.document.get_parameter(mn.disp_ex,
                                                    section3[0], "Material")

# make a simple coil
coil1 = em.make_simple_coil(mn.doc, 1, section1)

# assign relevant parameters to excite the coil
i_dc = 10
em.set_parameter(mn.doc, coil1, "WaveFormType", "DC", mn.consts)
em.set_parameter(mn.doc, coil1, "Current", i_dc, mn.consts)

curr = em.tool_magnet.document.document.get_parameter(mn.disp_ex,
                                                     coil1, "Current")

"""
sin_offset = 0
sin_mag = 10
ArrayValues = [sin_offset, sin_mag]
MagnetFunc.setParameter(Doc,  coil1, "WaveFormType", "SIN", MNConsts)
MagnetFunc.setParameter(Doc,  coil1, "WaveFormValues", ArrayValues, MNConsts)
"""

# make a motion component
motion = em.make_motion_component(mn.doc, section3)

# assign relevant parameters for the motion component
position_at_startup = 0
speed_at_startup = 0
time_array = 0
speed_array = 1000
time_speed = [time_array, speed_array]
direction = [0, 0, -1]
# set parameters for the motion component
em.set_parameter(mn.doc, motion, "MotionSourceType",
                "VelocityDriven", mn.consts)
em.set_parameter(mn.doc, motion, "MotionType", "Rotary", mn.consts)
em.set_parameter(mn.doc, motion, "PositionAtStartup",
                position_at_startup, mn.consts)
em.set_parameter(mn.doc, motion, "SpeedAtStartup", speed_at_startup, mn.consts)
em.set_parameter(mn.doc, motion, "MotionDirection", direction, mn.consts)
em.set_parameter(mn.doc, motion, "SpeedVsTime", time_speed, mn.consts)
