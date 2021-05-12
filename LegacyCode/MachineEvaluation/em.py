# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:02:41 2021

@author: Martin Johnson
"""

import sys
sys.path.append("...")
import macheval as me
from typing import Any
from copy import deepcopy

class EMProblemDefinition(me.ProblemDefinition):
    """Class converts input state into a problem"""
    
    def getProblem(self,state:'me.State')->'me.Problem':
        """Returns Problem from Input State"""
        #TODO define problem definition
        args=None
        problem=EMProblem(args)
        return problem

class EMProblem():
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
        
    
class EMAnalyzer(me.Analyzer):
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
    


class EMPostAnalyzer(me.PostAnalyzer):
    """Converts input state into output state for TemplateAnalyzer"""
    def getNextState(self,results:Any,stateIn:'me.State')->'me.State':
        stateOut=deepcopy(stateIn)
        #TODO define Post-Analyzer
        return stateOut
    

class EMStep(me.AnalysisStep):
    def __init__(self,settings):
        self.problemDefinition=EMProblemDefinition(settings)
        self.analyzer= EMAnalyzer(settings)
        self.postAnalyzer=EMPostAnalyzer(settings)