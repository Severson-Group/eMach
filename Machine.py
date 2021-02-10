# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:43:32 2021

@author: Martin Johnson
"""
from abc import ABC, abstractmethod

class Machine(ABC):
    """ABC for Machine objects"""
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def check_for_required_values():
        pass
    

