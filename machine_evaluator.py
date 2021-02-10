# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:43:03 2021

@author: Martin Johnson
"""

class MachineEvaluator:
    """MachineEvaluator Converts free-variables to MachineEvaluations"""
    
    def __init__(self,architect: "Architect",analyzer:
                 "Analyzer",specification: "Specification"):
        """Initialize MachineFactory from an Architect and Evaluator
        
        Keyword Arguments:
            architech: Architect
            analyzer: Analyzer
            specification: Specification
        """
        
        self.architect=architect
        self.analyzer=analyzer
        self.specification=specification
    def machine_evaluation_from_free_variables(self,free_variables: list) -> "MachineEvaluation":
        """Converts free variables to machine evaluation
        
        Keyword Arguments:
            free_variables: list 
            
        Return Values
            machine_evaluation: Evaluation Object
        """
        op_point=self.specification.op_point
        machine=self.architect.create_new_design(free_variables,specification)
        machine_evaluation=self.analyze.analyze(machine,op_point)
        return machine_evaluation
    def get_bounds(self) -> "array":
        """Gets bounds for optimization problem"""
        
        return self.specification.get_bounds()
    
    def set_specification(specification: 'Specification'):
        """Sets the specification for the MachineEvaluator"""
        self.specification=specification
        
    
    
    