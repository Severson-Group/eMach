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

class SleeveDesignProblemDefinition(me.ProblemDefinition):
    """Class converts input state into a problem"""
    
    def getProblem(self,state:'me.State')->'me.Problem':
        """Returns Problem from Input State"""
        #TODO define problem definition
        args=None
        problem=SleeveDesignProblem(args)
        return problem

class SleeveDesignProblem():
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
        
    
class SleeveDesignAnalyzer(me.Analyzer):
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
    


class SleeveDesignPostAnalyzer(me.PostAnalyzer):
    """Converts input state into output state for TemplateAnalyzer"""
    def getNextState(self,results:Any,stateIn:'me.State')->'me.State':
        stateOut=deepcopy(stateIn)
        #TODO define Post-Analyzer
        return stateOut
    

class SleeveDesignStep(me.AnalysisStep):
    def __init__(self,settings):
        self.problemDefinition=SleeveDesignProblemDefinition(settings)
        self.analyzer= SleeveDesignAnalyzer(settings)
        self.postAnalyzer=SleeveDesignPostAnalyzer(settings)