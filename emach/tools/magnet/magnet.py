# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:51:18 2020

@author: Bharat
"""
from win32com.client import DispatchEx
from ..tool_abc import toolabc as abc

from . import document
from .document import *

__all__ = []
__all__ += document.__all__
__all__ += ["MagNet"]

for i in range(len(document.document.__all__)):
    __all__.remove(document.document.__all__[i])

class MagNet(abc.ToolBase, abc.DrawerBase, abc.MakerExtrudeBase, abc.MakerRevolveBase):
    """ A class to represent a MAGNET file
    """

    def __init__(self):
        pass

    def open(self, i_filename=None, i_visible=False):
        """ opens a new MAGNET session and assigns variables neccessary for further
        operations
        """

        self.disp_ex = DispatchEx("MagNet.Application")  # Opens a new MAGNET session
        self.disp_ex.visible = i_visible  # Makes MAGNET window visible
        if i_filename is str:
            self.doc = self.disp_ex.openDocument(i_filename)
        else:
            self.doc = self.disp_ex.newDocument()
        self.view = self.doc.getView()
        self.sol = self.doc.getSolution()
        self.consts = self.disp_ex.getConstants()  # Get MAGNET Constants

    def close(self):
        pass

    def draw_line(self, startxy, endxy):
        """
        Draws a line in MAGNET

        Parameters
        ----------
        startxy : integer list of len 2
            the starting coordinate of the line
        endxy : Tinteger list of len 2
            the ending coordinate of the line

        Raises
        ------
        TypeError
            If the coomand can't be passed to MAGNET due to any reason.

        Returns
        -------
        ret : int
            0 if successful 1 if failed.

        """
        try:
            ret = self.view.newLine(startxy[0], startxy[1], endxy[0], endxy[1])
            return ret
        except:
            raise TypeError

    def draw_arc(self, centrexy, startxy, endxy):
        """
        Draws an arc in MAGNET

        Parameters
        ----------
        centrexy : integer list of len 2
            the centre coordinate of the arc.
        startxy : integer list of len 2
            the starting coordinate of the arc
        endxy : Tinteger list of len 2
            the ending coordinate of the arc

        Returns
        -------
        ret : int
            0 if successful 1 if failed.

        """
        ret = self.view.newArc(
            centrexy[0], centrexy[1], startxy[0], startxy[1], endxy[0], endxy[1]
        )
        return ret

    def select(self):
        pass

    def prepare_section(self, inner_coord):
        """
        Selects a section in MAGNET

        Parameters
        ----------
        inner_coord : integer list of len 2
            coordinate within section user wishes to select.

        Returns
        -------
        None.

        """
        self.view.selectAt(
            inner_coord[0],
            inner_coord[1],
            self.consts.infoSetSelection,
            [self.consts.infoSliceSurface],
        )

    def extrude(self, name, material, depth, token=None):
        """
        Extrudes, assigns a material and name to a selected section in MAGNET
        """
        if token is None:
            ret = self.view.makeComponentInALine(
                depth,
                name,
                "Name=" + material,
                self.consts.infoMakeComponentUnionSurfaces
                or self.consts.infoMakeComponentRemoveVertices,
            )
        else:
            ret = self.View.makeComponentInALine(depth, name, "Name=" + material, token)
        return ret

    def revolve(self, name, material, center, axis, angle, token=None):
        """
        Revloves, assigns a material and name to a selected section in MAGNET
        """
        if token is None:
            ret = self.view.makeComponentInAnArc(
                center[0],
                center[1],
                axis[0],
                axis[1],
                angle,
                name,
                "Name=" + material,
                self.consts.infoMakeComponentUnionSurfaces
                or self.consts.infoMakeComponentRemoveVertices,
            )
        else:
            ret = self.view.makeComponentInAnArc(
                center[0],
                center[1],
                axis[0],
                axis[1],
                angle,
                name,
                "Name=" + material,
                token,
            )
        return ret
