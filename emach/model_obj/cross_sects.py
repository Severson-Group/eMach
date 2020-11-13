# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 22:56:54 2020

@author: Bharat
"""
import numpy as np
from .cross_sect_base import CrossSectBase, CrossSectToken


class HollowCylinder(CrossSectBase):
    """
    this is a class to represent the crossection of a hollow cyclinder
    """

    def __init__(self, name, dim_d_a, dim_r_o, location):
        self.name = name
        self.dim_d_a = dim_d_a
        self.dim_r_o = dim_r_o
        self.location = location

    def draw(self, drawer):
        """


        Parameters
        ----------
        drawer :
            instance of the tool in which you would like to draw the
            crossection

        Returns
        -------
        cs_token : LIST
            cs_token returns an inner coordinate within the crossection and
            paths of the segments used to draw the crossection.

        """

        x_coords = [0, 0, 0, 0]
        y_out = self.dim_r_o
        y_in = self.dim_r_o - self.dim_d_a
        y_coords = [-y_out, y_out, -y_in, y_in]
        coords = np.transpose(np.array([x_coords, y_coords]))

        points = self.location.trans_coord(coords)

        arc_out1 = drawer.draw_arc(self.location.anchor_xy, points[0, :], points[1, :])
        arc_out2 = drawer.draw_arc(self.location.anchor_xy, points[1, :], points[0, :])
        arc_out3 = drawer.draw_arc(self.location.anchor_xy, points[2, :], points[3, :])
        arc_out4 = drawer.draw_arc(self.location.anchor_xy, points[3, :], points[2, :])

        rad = self.dim_r_o - self.dim_d_a / 2
        inner_coord = self.location.trans_coord(np.array([[rad, 0]]))
        token = [arc_out1, arc_out2, arc_out3, arc_out4]

        cs_token = CrossSectToken(inner_coord[0, :], token)
        return cs_token

    def create_props(self):
        pass
