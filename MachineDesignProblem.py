# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:49:03 2021

@author: Martin Johnson
"""

class MachineDesignProblem:
    """User defined problem UDP utilized by PYGMO Problem class"""
    
    def __init__(self,machine_evaluator: "MachineEvaluator",objectives: "Objectives",data_handler: "DataHandler"):
        """Creates Machine Design problem
        
        Keyword Arguments:
            machine_evaluator: MachineEvaluator
            objectives: Objectives
        """
        self.machine_evaluator=machine_evaluator
        self.objectives=objectives
        self.dh=data_handler
        
    def fitness(self,free_variables: list):
        """Calculates fitness values from free variables""" 
        
        machine_evaluation=self.machine_evaluator.machine_evaluation_from_free_variables(free_variables)
        obj_results=self.objectives.get_objectives(machine_evaluation)
        self.dh.save_evaluation(machine_evaluation,free_variables,obj_results)
        return tuple(obj_results)
    
    def get_bounds(self):
        """Returns bounds for optimization problem""" 
        return tuple(self.machine_evaluator.get_bounds())
    def get_nobj(self):
        """Returns number of objectievs of optimization problem"""
        return self.objectives.get_nobj()        
    