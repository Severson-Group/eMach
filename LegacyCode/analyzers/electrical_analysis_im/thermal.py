# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:21:56 2021

@author: Martin Johnson
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:17:00 2021

@author: Martin Johnson
"""

import sys
sys.path.append("...")
import macheval as me
from typing import Any
from copy import deepcopy

class ThermalProblemDefinition(me.ProblemDefinition):
    """Class converts input state into a problem"""
    
    def getProblem(self,state:'me.State')->'me.Problem':
        """Returns Problem from Input State"""
        #TODO define problem definition
        args=None
        problem=ThermalProblem(args)
        return problem

class ThermalProblem():
    """problem class utilized by the Analyzer
    
    Attributes:
        TODO
    """
    def __init__(self,args):
        """Creates problem class
        
        Args:
            TODO
            
        """
        #TODO define problem 
        
    
class ThermalAnalyzer(me.Analyzer):
    """"Class Analyzes the CubiodProblem  for volume and Surface Areas"""
    
    def analyze(self,problem:'me.Problem'):
        """Performs Analysis on a problem

        Args:
            problem (me.Problem): Problem Object

        Returns:
            results (Any): 
                Results of Analysis

        """
        #TODO Define Analyzer
        results = []
        return results
    


class ThermalPostAnalyzer(me.PostAnalyzer):
    """Converts input state into output state for TemplateAnalyzer"""
    def getNextState(self,results:Any,stateIn:'me.State')->'me.State':
        stateOut=deepcopy(stateIn)
        #TODO define Post-Analyzer
        return stateOut
    

class ThermalStep(me.AnalysisStep):
    def __init__(self,settings):
        self.problemDefinition=ThermalProblemDefinition(settings)
        self.analyzer= ThermalAnalyzer(settings)
        self.postAnalyzer=ThermalPostAnalyzer(settings)