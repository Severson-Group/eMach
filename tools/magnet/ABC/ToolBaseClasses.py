# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:51:18 2020

@author: Bharat
"""

from win32com.client import DispatchEx
import AbstractBaseClasses as abc

class MagNet(abc.ToolBase, abc.DrawerBase, abc.MakerExtrudeBase, abc.MakerRevolveBase):
    def __init__(self):
        pass
    def open(self, iFilename = None, iMn = None, iVisible = False):
        self.MN = DispatchEx("MagNet.Application") #Opens a new MAGNET session
        self.MN.Visible = iVisible #Makes MAGNET window visible
        if iFilename is str:
            self.Doc = self.MN.openDocument(iFilename)
        else:
            self.Doc = self.MN.newDocument()
        self.View = self.Doc.getView()
        self.Sol = self.Doc.getSolution()
        self.MNConsts = self.MN.getConstants() #Get MAGNET Constants
        #self.Doc.setDefaultLengthUnit(defaultLength, True);
        
    def close(self): pass
    
    def drawLine(self, startxy, endxy):
        try:
            y = self.View.newLine(startxy[0], startxy[1], endxy[0], endxy[1])
            return y
        except:
            print('Invalid arguments for drawLine')

    def drawArc(self, centrexy, startxy, endxy):
        return self.View.newArc(centrexy[0], centrexy[1], startxy[0], startxy[1], endxy[0], endxy[1])
    
    def select(self):
        pass
    
    def prepareSection(self,innerCoord): 
        self.View.selectAt(innerCoord[0], innerCoord[1], self.MNConsts.infoSetSelection, [self.MNConsts.infoSliceSurface])
    
    def extrude(self,name,material,depth,token = None):
        if token == None:
            y = self.View.makeComponentInALine(depth, name, "Name="+material, self.MNConsts.infoMakeComponentUnionSurfaces 
                                      or self.MNConsts.infoMakeComponentRemoveVertices)
        else:
            y = self.View.makeComponentInALine(depth, name, "Name="+material, token)           
        return y

    def revolve(self, name, material, center, axis, angle, token=None):
        if token == None:
            y = self.View.makeComponentInAnArc(center[0], center[1], axis[0], axis[1], angle, name, "Name="+material, 
                                       self.MNConsts.infoMakeComponentUnionSurfaces or self.MNConsts.infoMakeComponentRemoveVertices)
        else:
            y = self.View.makeComponentInAnArc(center[0], center[1], axis[0], axis[1], angle, name, "Name="+material, token)            
        return y