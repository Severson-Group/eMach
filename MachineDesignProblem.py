# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:49:03 2021

@author: Martin Johnson
"""

class MachineDesignProblem:
    """User defined problem UDP utilized by PYGMO Problem class"""
    
    def __init__(self,machine_factory,objectives,data_handler):
        """Creates Machine Design problem
        
        Keyword Arguments:
            machine_designer: MachineDesigner
            objectives: Objectives
        """
        self.machine_factory=machine_factory
        self.objectives=objectives
        self.dh=data_handler
        
    def fitness(self,free_variables):
        """Calculates fitness values from free variables""" 
        
        design_evaluation=self.machine_designer.new_design_from_free_variables(free_variables)
        obj_results=self.objectives.get_objectives(design_evaluation)
        self.dh.save_design(design_evaluation,free_variables,obj_results)
        return tuple(obj_results)
    
    def get_bounds(self):
        """Returns bounds for optimization problem""" 
        return tuple(self.machine_factory.get_bounds())
    def get_nobj(self):
        """Returns number of objectievs of optimization problem"""
        return int(len(self.objectives.obj_names))        
    