# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 11:14:54 2021

@author: Martin Johnson
"""
from abc import ABC, abstractmethod

class Analyzer(ABC):
    """This is the Analyzer ABC, it is used to extract results from a machine
    object. This is where the analysis of a machine in the optimization 
    process will occur.    
    """
    
    @abstractmethod
    def __init__(self):
        """Initialize Analyzer"""
        pass
    
    @abstractmethod
    def analyze(self,machine: "Machine",op_point: "OperatingPoint") -> "AnalysisResults":
        """This function takes in the machine to be analyzed, and an operating
        point, completes some calculation and returns an Evaluation Object
        
        Keyword Argument:
            machine: Machine
            op_point: Dict
            
        Return Value:
            analysis_results: AnalysisResults
        """
        
        return analysis_results
    
    
    
