# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 11:26:45 2021

@author: Martin Johnson
"""

from abc import ABC, abstractmethod

class Architect(ABC):
    """The architect abc class. This class is the interface between a 
    machine object and the design framework. All the math for calculating an
    Inital Design is done in this object, and a design dictionary is passed
    into the Machine object class on creatation"""
    
    @abstractmethod
    def __init__(self):
        """Initialize the Architect"""
        pass
    
    @abstractmethod
    def create_new_design(self,input_arguments) -> "Machine":
        """This creates a new Machine object and returns it
        
        Keyword arguments:
            input_arguments: any
        
        Return Values:
            machine: Machine
        """
        pass

