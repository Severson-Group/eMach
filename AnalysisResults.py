# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 09:27:04 2021

@author: Martin Johnson
"""


class AnalysisResults:
    """This class stores the results of from an analyzer"""
    def __init__(self,machine: "Machine",op_point: "OperatingPoint",results):
        """Creates Evaluation object 
        
        Keyword Arguments:
            machine: Machine
            specification: dict
            results: dict
        """
        self.machine = machine
        self.op_point = op_point
        self.results = results
    

    