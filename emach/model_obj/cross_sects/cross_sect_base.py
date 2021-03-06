# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 23:22:49 2020

@author: Bharat
"""
from abc import ABC, abstractmethod
from typing import List

class CrossSectBase(ABC):
    @abstractmethod
    def draw(self, drawer: any) -> 'CrossSectToken': 
        '''
        Function to draw cross-sections using any drawer supported by eMach

        Parameters
        ----------
        drawer : any
            DESCRIPTION. Drawer tool supported in eMach having draw_line and 
            draw_arc methods

        Returns
        -------
        cs_token : CrossSectToken
            DESCRIPTION. Wrapper object holding information of inner coordinate
            of cross-section and tokens representing the cross-section

        '''
        pass
    

class CrossSectToken():
    
    def __init__(self, inner_coord: List['DimLinear'], token: List['TokenDraw']):
        self.__inner_coord = inner_coord
        self.__token = token
        
    @property
    def inner_coord(self):
        return self.__inner_coord
    
    @property
    def token(self):
        return self.__token