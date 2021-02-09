# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 11:26:45 2021

@author: Martin Johnson
"""

from abc import ABC, abstractmethod

class Architect(ABC):
    """The architect abc class """
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def create_new_design(self):
        pass
    

