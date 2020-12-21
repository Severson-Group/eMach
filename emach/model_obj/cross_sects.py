# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 22:56:54 2020

@author: Bharat
"""
import numpy as np
from jsonschema import validate

from .cross_sect_base import CrossSectBase, CrossSectToken


class HollowCylinder(CrossSectBase):
    
    def __init__(self, name, dim_d_a, dim_r_o, location): 
            
        self.name = name;
        self.__dim_d_a = dim_d_a;
        self.__dim_r_o = dim_r_o;
        self.location = location;
    
    @property
    def dim_d_a(self):
        return self.__dim_d_a
    
    @property
    def dim_r_o(self):
        return self.__dim_r_o
    
    
    def draw(self, drawer):
        r = self.__dim_r_o
        t = self.__dim_d_a
        
        x_out = 0
        x_in = 0
        x = [x_out, x_out, x_in, x_in]
        y_out = r
        y_in = r-t
        y = [-y_out, y_out, -y_in, y_in]
        z = np.array([x, y])
        coords = np.transpose(z)
        
        p = self.location.trans_coord(coords)
        
        arc_out1 = drawer.draw_arc(self.location.anchor_xy, p[0,:], p[1,:])
        arc_out2 = drawer.draw_arc(self.location.anchor_xy, p[1,:], p[0,:])
        arc_out3 = drawer.draw_arc(self.location.anchor_xy, p[2,:], p[3,:])
        arc_out4 = drawer.draw_arc(self.location.anchor_xy, p[3,:], p[2,:])
        
        rad = r - t*0.5
        inner_coord = self.location.trans_coord(np.array([[rad, 0]]))
        token = [arc_out1, arc_out2, arc_out3, arc_out4]
        
        cs_token = CrossSectToken(inner_coord[0,:], token)
        return cs_token
        
        
    def create_props(self): pass
        