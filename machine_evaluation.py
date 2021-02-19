# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 09:27:04 2021

@author: Martin Johnson
"""


class MachineEvaluation:
    """This class stores the results of from an MachineEvaluator"""
    def __init__(self,specification: "Specification",analysis_results: "AnalysisResults"):
        """Creates MachineEvaluation object 
        
        Keyword Arguments:
            specification: Specification
            analysis_results: AnalysisResults
        """
        self.specification = specification
        self.analysis_results = analysis_results
    

    