# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 17:58:20 2020

@author: Bharat
"""
#File containing all the user defined MagNet functions and the pywin32 library needed for VBS
import MagnetFunc  

#Launch MagNet application and make window visible
MN = MagnetFunc.launch()

#Get Handles to MAGNET Scripting Interfaces
[Doc, View, Circuit, MNConsts] = MagnetFunc.init(MN)

#set Default length unit as millimeters
Doc.setDefaultLengthUnit("millimeters", True)

#draw circles with x,y as the coordinates of the centre, r as the radius
MagnetFunc.drawCircle(View, 0, 0, 20)
MagnetFunc.drawCircle(View, 0, 0, 30)
MagnetFunc.drawCircle(View, 0, 0, 50)

#select section 
MagnetFunc.selectSection(View, MNConsts,-1, 0)
#assign parameters needed for extrusion
section1 = "conductor"
material = 'Copper: 100% IACS'
sweepDist = 10
#extrude selected section by the distance specified in sweepDist with material and section name as provided. 
sweep1Status = MagnetFunc.makeComponentInALine(MN, MNConsts, sweepDist, section1, material)


MagnetFunc.selectSection(View, MNConsts,-25, 0)
section2 = "air"
material = 'AIR'
sweepDist = 10
#extrude selected section by the distance specified in sweepDist with material and section name as provided
sweep2Status = MagnetFunc.makeComponentInALine(MN, MNConsts, sweepDist, section2, material)

MagnetFunc.selectSection(View, MNConsts,-35, 0,)
section3 = "iron"
material = 'Arnon 5'
sweepDist = 10
#extrude selected section by the distance specified in sweepDist with material and section name as provided
sweep3Status = MagnetFunc.makeComponentInALine(MN, MNConsts, sweepDist, section3, material)

#make a simple coil
coil1 = MagnetFunc.makeSimpleCoil(Doc, 1, section1)

#assign relevant parameters to excite the coil
Idc = 10
MagnetFunc.setParameter(Doc, coil1, "WaveFormType", "DC", MNConsts)
MagnetFunc.setParameter(Doc, coil1, "Current", Idc, MNConsts)

'''
sin_offset = 0
sin_mag = 10
ArrayValues = [sin_offset, sin_mag]
MagnetFunc.setParameter(Doc,  coil1, "WaveFormType", "SIN", MNConsts)
MagnetFunc.setParameter(Doc,  coil1, "WaveFormValues", ArrayValues, MNConsts)
'''

#make a motion component
motion = MagnetFunc.makeMotionComponent(Doc,['iron'])

#assign relevant parameters for the motion component
positionAtStartup = 0
speedAtStartup = 0
timeArray = 0
speedArray = 1000
timespeed = [timeArray, speedArray]
direction = [0,0,-1]
#set parameters for the motion component
MagnetFunc.setParameter(Doc, motion, 'MotionSourceType','VelocityDriven', MNConsts)
MagnetFunc.setParameter(Doc, motion, 'MotionType','Rotary', MNConsts)
MagnetFunc.setParameter(Doc, motion, 'PositionAtStartup',positionAtStartup, MNConsts)
MagnetFunc.setParameter(Doc, motion, 'SpeedAtStartup',speedAtStartup, MNConsts)
MagnetFunc.setParameter(Doc, motion, 'SpeedVsTime', timespeed, MNConsts)
MagnetFunc.setParameter(Doc, motion, 'MotionDirection', direction, MNConsts)


