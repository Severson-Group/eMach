# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 10:56:43 2021

@author: Martin Johnson
"""

from abc import ABC, abstractmethod

class OperatingPoint(ABC):
    """ABC which holds information on the operating point of a machine"""
   
    @abstractmethod
    def __init__(self):
        """Create OperatingPoint class"""
        
    