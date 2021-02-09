# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:54:52 2021

@author: Martin Johnson
"""
from abc import ABC, abstractmethod


class Objectives(ABC):
    """The Objectives class is used to store the names of the objectives as 
    well as the function get objectives which returns the objective values
    used by pygmo"""
    @abstractmethod
    def __init__(self):
        """Creates objectives object"""
    
    @abstractmethod
    def get_objectives(self,design_evaluation):
        """ Calculates objectives from a design_evaluation
        Keyword Arguments:
            design_evaluation: Evaluation 
            
        Return Values:
            objs: list
        """
    
        return objs
