from win32com.client import DispatchEx

from ..tool_abc import toolabc as abc
from ..token_draw import TokenDraw
from . import document
from .document import *
from ...model_obj.dimensions import *


__all__ = []
__all__ += ["MagNet"]


class MagNet(abc.ToolBase, abc.DrawerBase, abc.MakerExtrudeBase, abc.MakerRevolveBase):
    """ A class to handle MagNet applications
    """

    def __init__(self):
        self.disp_ex = None
        self.doc = None
        self.view = None
        self.sol = None
        self.consts = None
        self.default_length = 'DimMillimeter'
        self.default_angle = 'DimDegree'

    def open(self, filename=None, visible=False):
        """ opens a new MAGNET session and assigns variables neccessary for further
        operations
        """

        self.disp_ex = DispatchEx("MagNet.Application")  # Opens a new MAGNET session
        self.disp_ex.visible = visible  # Makes MAGNET window visible
        if filename is str:
            self.doc = self.disp_ex.openDocument(filename)
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
        start_x = eval(self.default_length)(startxy[0])
        start_y = eval(self.default_length)(startxy[1])
        end_x = eval(self.default_length)(endxy[0])
        end_y = eval(self.default_length)(endxy[1])

        ret = self.view.newLine(start_x, start_y, end_x, end_y)
        
        self.disp_ex.setVariant(0, 'line', 'python')
        line = self.disp_ex.getVariant(0, 'python');
        
        return TokenDraw(line,0)


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
        ret : TokenDraw object

        """
        centre_x = eval(self.default_length)(centrexy[0])
        centre_y = eval(self.default_length)(centrexy[1])
        start_x = eval(self.default_length)(startxy[0])
        start_y = eval(self.default_length)(startxy[1])
        end_x = eval(self.default_length)(endxy[0])
        end_y = eval(self.default_length)(endxy[1])
        
        ret = self.view.newArc(
            centre_x, centre_y, start_x, start_y, end_x, end_y
        )
        
        self.disp_ex.setVariant(0, 'arc', 'python')
        arc = self.disp_ex.getVariant(0, 'python');
        
        return TokenDraw(arc,1)

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
        inner_coord_x = eval(self.default_length)(inner_coord[0])
        inner_coord_y = eval(self.default_length)(inner_coord[1])
        
        self.view.selectAt(
            inner_coord_x,
            inner_coord_y,
            self.consts.infoSetSelection,
            [self.consts.infoSliceSurface],
        )

    def extrude(self, name, material, depth, token = None):
        """
        Extrudes, assigns a material and name to a selected section in MAGNET
        """
        depth_actual = eval(self.default_length)(depth)
        
        ret = self.view.makeComponentInALine(
                depth_actual,
                name,
                "Name=" + material,
                self.consts.infoMakeComponentRemoveVertices
            )

        return ret

    def revolve(self, name, material, center, axis, angle, token = None):
        """
        Revloves, assigns a material and name to a selected section in MAGNET
        """
        center_x = eval(self.default_length)(center[0])
        center_y = eval(self.default_length)(center[1])
        axis_x = eval(self.default_length)(axis[0])
        axis_y = eval(self.default_length)(axis[1])
        angle_actual = eval(self.default_length)(angle)
        
        ret = self.view.makeComponentInAnArc(
                center_x,
                center_y,
                axis_x,
                axis_y,
                angle_actual,
                name,
                "Name=" + material,
                self.consts.infoMakeComponentRemoveVertices,
            )
        
        return ret
    
    def view_all(self):
        '''
        Function to view entire cross-section of drawing made in MagNer

        '''
        self.view.viewAll()
        
    def set_default_length(self, user_unit, make_app_default):
        '''
        Function to set the default length unit in MagNet. Supports millimeters
        and inches.

        Parameters
        ----------
        user_unit : str
            DESCRIPTION. String representing the unit the user wishes to set
            as default.
        make_app_default : bool
            DESCRIPTION. Boolean with which user can set a unit as the default
            unit employed in MagNet

        Raises
        ------
        TypeError
            DESCRIPTION. Raise a TypeError if incorrent dimension is passed

        Returns
        -------
        None.

        '''
        
        if (user_unit == 'millimeters'):
            self.default_length = 'DimMillimeter'
        elif (user_unit == 'inches'):
            self.default_length = 'DimInch'
        else:
            raise TypeError
        
        self.doc.setDefaultLengthUnit(user_unit, make_app_default)
