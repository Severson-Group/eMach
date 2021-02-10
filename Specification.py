# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 11:03:46 2021

@author: Martin Johnson
"""
from abc import ABC, abstractmethod

class Specification(ABC):
    """ABC which holds information on the specification of a machine"""
   
    @abstractmethod
    def __init__(self):
        """Create Specification class"""
        
    