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
    def get_objectives(self,machine_evaluation: "MachineEvaluation"):
        """ Calculates objectives from a machine_evaluation
        Keyword Arguments:
            machine_evaluation: MachineEvaluation 
            
        Return Values:
            objs: list
        """
    
        return objs

    def get_nobj(self):
        "return number of objectives"
        
        return nobj