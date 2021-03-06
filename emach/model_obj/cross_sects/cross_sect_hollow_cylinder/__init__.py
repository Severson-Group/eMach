# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 16:12:27 2021

@author: Bharat
"""

import numpy as np

from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectHollowCylinder']
class CrossSectHollowCylinder(CrossSectBase):
    
    def __init__(self, name: str, dim_d_a: 'DimLinear', dim_r_o: 'DimLinear', \
                 location: 'Location2D') -> None: 
        '''
        Intialization function for HollowCylinder class. This function takes in
        arguments and saves the information passed to private variable to make
        them read-only

        Parameters
        ----------
        name : str
            DESCRIPTION. This is the name the user wishes to provide to the 
            hollow cylinder cross-section.
        dim_d_a : DimLinear
            DESCRIPTION. Thickness of the cylinder.
        dim_r_o : DimLinear
            DESCRIPTION. Outer radius of the cylinder: class type dimLinear
        location : Location2D
            DESCRIPTION. Object of Location2D class providing information on 
            cross-sect anchor and angle of orientation with respect to the 
            origin

        Returns
        -------
        None
        '''
        self.__name = name;
        self.__dim_d_a = dim_d_a;
        self.__dim_r_o = dim_r_o;
        self.__location = location;
    
    @property
    def dim_d_a(self):
        return self.__dim_d_a
    
    @property
    def dim_r_o(self):
        return self.__dim_r_o
    
    @property
    def name(self):
        return self.__name
    
    @property
    def location(self):
        return self.__location
    
    def draw(self, drawer):

        r = self.__dim_r_o # outer radius of hollow cylinder
        t = self.__dim_d_a # thickness of hollow cylinder
        
        x_out = type(r)(0) # assign intial origin as DimLinear object of 0
        x_in = type(r)(0)
        x = [x_out, x_out, x_in, x_in]
        
        y_out = r
        y_in = r-t
        y = [-y_out, y_out, -y_in, y_in]
        z = np.array([x, y])
        
        coords = np.transpose(z)# convert coordinates to a form of [[x1,y1]..]
        
        p = self.location.trans_coord(coords) # shift coordinates based on anchor and theta given in location
        
        # draw hollow cylinder
        arc_out1 = drawer.draw_arc(self.location.anchor_xy, p[0,:], p[1,:])
        arc_out2 = drawer.draw_arc(self.location.anchor_xy, p[1,:], p[0,:])
        arc_out3 = drawer.draw_arc(self.location.anchor_xy, p[2,:], p[3,:])
        arc_out4 = drawer.draw_arc(self.location.anchor_xy, p[3,:], p[2,:])
        
        # get coordinate within hollow cylinder
        rad = r - t*0.5 
        inner_coord = self.location.trans_coord(np.array([[rad, type(r)(0)]]))
        
        token = [arc_out1, arc_out2, arc_out3, arc_out4] # compile tokens
        
        cs_token = CrossSectToken(inner_coord[0,:], token) # create CrossSectToken object
        return cs_token
        
        
