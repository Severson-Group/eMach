# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 23:22:49 2020

@author: Bharat
"""
from abc import ABC, abstractmethod

class CrossSectBase(ABC):
    @abstractmethod
    def draw(self, drawer): pass
    

class CrossSectToken():
    
    def __init__(self, inner_coord, token):
        self.__inner_coord = inner_coord
        self.__token = token
        
    @property
    def inner_coord(self):
        return self.__inner_coord
    
    @property
    def token(self):
        return self.__token