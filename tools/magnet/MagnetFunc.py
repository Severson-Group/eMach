# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 14:07:59 2020

@author: Ramadas
"""
#Needed at the beginning to use pywin32 to call ActiveX compliant programs as COM automation servers
from win32com.client import DispatchEx 

def launch():
    MN = DispatchEx("MagNet.Application")   #open MagNet
    MN.Visible = True                       #make the MagNet window visible
    return MN

def init(MN):
    #Get Handles to MAGNET Scripting Interfaces
    Doc = MN.newDocument()                  
    View = Doc.getView()
    Circuit = Doc.getCircuit()
    MNConsts = MN.getConstants() 
    return Doc, View, Circuit, MNConsts

def drawCircle(View, x, y, r):
    #draw circle with x,y as the coordinates of the centre, r as the radius
    View.newCircle(x, y, r)
    View.viewAll()
    
def selectSection(View, MNConsts, x, y):
    #select section containing coordinate (x,y)
    View.selectAt(x, y, MNConsts.infoSetSelection)

'''
def makeComponentInALine(View, MNConsts, sweepDist, sectionName, material, flag=5):
    if flag ==1:
        View.makeComponentInALine(sweepDist, sectionName, "Name="+material, MNConsts.infoMakeComponentUnionSurfaces)
    elif flag ==2:
        View.makeComponentInALine(sweepDist, sectionName, "Name="+material, MNConsts.infoMakeComponentIgnoreHoles)
    elif flag ==3:
        View.makeComponentInALine(sweepDist, sectionName, "Name="+material, MNConsts.infoMakeComponentRemoveVertices)
    elif flag ==4:
        View.makeComponentInALine(sweepDist, sectionName, "Name="+material, MNConsts.infoMakeComponentUnionSurfaces or 
                                  MNConsts.infoMakeComponentIgnoreHoles)
    elif flag ==5:
        View.makeComponentInALine(sweepDist, sectionName, "Name="+material, MNConsts.infoMakeComponentUnionSurfaces or 
                                  MNConsts.infoMakeComponentRemoveVertices)
    elif flag ==6:
        View.makeComponentInALine(sweepDist, sectionName, "Name="+material, MNConsts.infoMakeComponentIgnoreHoles or 
                                  MNConsts.infoMakeComponentRemoveVertices)
    else:
        View.makeComponentInALine(sweepDist, sectionName, "Name="+material, MNConsts.infoMakeComponentUnionSurfaces or 
                                  MNConsts.infoMakeComponentIgnoreHoles or MNConsts.infoMakeComponentRemoveVertices)       
'''

def makeComponentInALine(MN, MNConsts, sweepDist, sectionName, material):
    '''command to extrude a selected section by 'sweepDis't and assign to the component the 'sectionName' and 'material' 
    as specified, returns 0 if extrusion is succesful, 1 if extrusion failed'''
    MN.processCommand("REDIM ArrayOfValues(0)")
    MN.processCommand("ArrayOfValues(0) = \"{}\"".format(sectionName))
    MN.processCommand("ret = getDocument.getView.makeComponentInALine({}, ArrayOfValues, \"Name={}\")"
                      .format(sweepDist,material))
    MN.processCommand("Call setVariant(0, ret)")    
    err = MN.getVariant(0)
    return err


def makeSimpleCoil(Doc, ProblemID, ArrayOfValues):
    #function to make a simple coil with 'ArrayOfValues' and 'ProblemID', returns path to the coil
    coil=Doc.makeSimpleCoil(ProblemID, ArrayOfValues)
    return coil
''' 
def newCircuitWindow(Doc):
    Doc.newCircuitWindow()
    
def insertCurrentSource(Doc, Circuit, x, y):
    Circuit.insertCurrentSource(x, y)
'''

def setParameter(Doc, opath, param, value, MNConsts):
    #sets parameter, 'param' of object with path 'opath' as 'value'
    if type(value) is str:
        Doc.setParameter(opath, param, value, MNConsts.infoStringParameter)
    elif type(value) is int:
        Doc.setParameter(opath, param, str(value), MNConsts.infoNumberParameter)
    elif type(value) is list:
        Doc.setParameter(opath, param, str(value), MNConsts.infoArrayParameter)
    
def makeMotionComponent(Doc,ArrayOfValues):
    #makes a Motion component of 'ArrayOfValues', returns path of the Motion component
    motion = Doc.makeMotionComponent(ArrayOfValues)
    return motion
