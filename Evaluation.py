# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 09:27:04 2021

@author: Martin Johnson
"""


class Evaluation:
    
    def __init__(self,machine,op_point,results):
        """Creates Evaluation object 
        
        Keyword Arguments:
            machine: Machine
            specification: dict
            results: dict
        """
        self.machine = machine
        self.op_point = op_point
        self.results = results
    

    