# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 10:59:45 2021

@author: Martin Johnson
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
sys.path.append("..")
import mach_opt as mo
import macheval as me
import pygmo as pg
from typing import List,Tuple,Any
from copy import deepcopy


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class TemplateArchitect(me.Architect):
    """Class converts input tuple x into a machine object"""    
    def create_new_design(self,x:tuple)->"me.Machine":
        """
        converts x tuple into a machine object.

        Args:
            x (tuple): Input free variables.
            
        Returns:
            machine (me.Machine): Machine object
        """
        
        #TODO Define Architect
        machine=TemplateMachine()
        return machine
    
class TemplateMachine(me.Machine):
    """Class defines a Machine object 
    
    Attributes:
        TODO
    """
    
    def __init__(self):
        """Creates a machine object.

        Args:
            TODO

        """
        
        #TODO Define Machine
        
        
    def check_required_properites():
        """Checks for required input properties"""
        #TODO 
        pass
    
    
    def get_missing_properties():
        """Returns missing input properites"""
        #TODO
        pass

    
class TemplateProblemDefinition(me.ProblemDefinition):
    """Class converts input state into a problem"""
    
    def getProblem(self,state:'me.State')->'me.Problem':
        """Returns Problem from Input State"""
        #TODO define problem definition
        args=None
        problem=TemplateProblem(args)
        return problem

class TemplateProblem():
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
        
    
class TemplateAnalyzer(me.Analyzer):
    """"Class Analyzes the CubiodProblem  for volume and Surface Areas"""
    
    def analyze(self,Problem:'me.Problem'):
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
    


class TemplatePostAnalyzer(me.PostAnalyzer):
    """Converts input state into output state for TemplateAnalyzer"""
    def getNextState(self,results:Any,stateIn:'me.State')->'me.State':
        stateOut=deepcopy(stateIn)
        #TODO define Post-Analyzer
        return stateOut
    

class ConstraintError(Error):
    """Error for violating optimization constraint"""
    def __init__(self,value):
        #TODO define error
        self.value=value

    
class TemplateConstraintEvaluationStep(me.EvaluationStep):
    """Constraint evaluation step template"""
    def step(self,stateIn):
        """Checks input state to see if constraint is violated
        
        Raises ConstraintError if violated, otherwise appends values to 
        State conditions and moves forward"""
        
        value = None #TODO define constraint
        if value >=0:
            raise ConstraintError(value)
        else:
            stateOut=deepcopy(stateIn)
            stateOut.stateConditions.constraintValue=value
            return [value,stateOut]
    
class TemplateObjective(mo.Objective):
    """Class defines objectives of cubiod optimization"""

    def getObjectives(self,results:"List[float,float]"):
        """ Calculates objectives from evaluation results
        

        Args:
            results (List): Results from MachineEvaluator

        Returns:
            Tuple: objectives tuple 
        """
        final_state=results[-1][-1]
        results=None #TODO define objectives
        return results
    
class DataHandler:
    def save(self,design,fullResults,objs):
        """Unimplented data handler"""
        #TODO Define datahandler
        pass

if __name__ == '__main__':
    
    #Create Designer
    settings=None #TODO define settings
    des=me.MachineDesigner(TemplateArchitect(),settings)

    #Create evaluation steps
    evalSteps=[TemplateConstraintEvaluationStep(),
               me.AnalysisStep(TemplateProblemDefinition(),
                               TemplateAnalyzer(),
                               TemplatePostAnalyzer())]#TODO define steps
    #Create Evaluator
    evaluator=me.MachineEvaluator(evalSteps)
    objectives=TemplateObjective()
    dh=DataHandler()
    
    #set evaluation bounds
    bounds=([0,0,0],[1,1,1])
    #set number of objectives
    n_obj=3
    
    #Create Machine Design Problem
    machDesProb=mo.MachineDesignProblem(des,evaluator,objectives,dh,
                                        bounds,n_obj)
    
    #Run Optimization
    opt=mo.MachineOptimizationMOEAD(machDesProb)
    pop=opt.run_optimization(496,10)
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits) 