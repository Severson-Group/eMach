"""
Created on Thu Oct  1 14:07:59 2020

@author: Bharat
"""

from win32com.client import DispatchEx  #module needed for opening MagNet

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
    View.selectAt(x, y, MNConsts.infoSetSelection, [MNConsts.infoSliceSurface])


def makeComponentInALine(View, MNConsts, sweepDist, ArrayOfValues, material):
    '''command to extrude a selected section by 'sweepDis't and assign to the component the 'sectionName' and 'material' 
    as specified, returns 0 if extrusion is succesful, 1 if extrusion failed'''
    y = View.makeComponentInALine(sweepDist, ArrayOfValues, "Name="+material, MNConsts.infoMakeComponentUnionSurfaces 
                                  or MNConsts.infoMakeComponentRemoveVertices)
    return y


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

def getParameter(MN, path, parameter):
    MN.processCommand("REDIM strArray(0)")
    MN.processCommand("DIM pType")
    MN.processCommand("pType = getDocument.getParameter(\"{}\", \"{}\", strArray)".format(path,parameter))
    MN.processCommand('Call setVariant(0, strArray,"PYTHON")')    
    param = MN.getVariant(0,"PYTHON")
    MN.processCommand('Call setVariant(0, pType,"PYTHON")')    
    param_type = MN.getVariant(0,"PYTHON")
    return param, param_type
