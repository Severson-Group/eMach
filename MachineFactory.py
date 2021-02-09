# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:43:03 2021

@author: Martin Johnson
"""

class MachineFactory:
    """MachineFactory creates a Machine from free variables and evaluates"""
    
    def __init__(self,architect,evaluator,specification):
        """Initialize MachineFactory from an Architect and Evaluator
        
        Keyword Arguments:
            architech: Architect
            evaluator: Evaluator
            specification: Dict
        """
        
        self.architect=architect
        self.analyzer=analyzer
        self.specification=specification
    def new_design_from_free_variables(self,free_variables):
        """Uses Architect to create a DesignVariant and Evaluator to evaluate design
        
        Keyword Arguments:
            free_variables: list 
            
        Return Values
            machine_evaluation: Evaluation Object
        """
        op_point=self.specification['op_point']
        machine=self.architect.create_new_design(free_variables,op_point)
        machine_evaluation=self.analyze.analyze(machine,op_point)
        return machine_evaluation
    def get_bounds(self):
        """Gets bounds for optimization problem"""
        
        return self.specification.get_bounds()
    
    def set_specification(specification):
        """Sets the specification for the factory"""
        self.specification=specification
        
    
    
    