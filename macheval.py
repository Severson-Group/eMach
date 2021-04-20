# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:54:48 2021

@author: Martin Johnson
"""

from typing import Protocol,runtime_checkable,Any
from abc import abstractmethod,ABC
from mach_opt import Design,Evaluator,Designer
from copy import deepcopy




class MachineDesign(Design):
    def __init__(self,machine:'Machine',setting: Any):
        self.machine=machine
        self.setting=setting 
        
class MachineDesigner(Designer):
    def __init__(self,arch:'Architect',settings:'Any'):
        self.arch=arch
        self.settings=settings
    def createDesign(self,x:'tuple')->'Design':
        machine=self.arch.create_new_design(x)
        design=MachineDesign(machine,self.settings)
        return design
        
class Architect(Protocol):
    """The architect abc class. This class is the interface between a 
    machine object and the design framework. All the math for calculating an
    Inital Design is done in this object, and a design dictionary is passed
    into the Machine object class on creatation"""
    
    
    @abstractmethod
    def create_new_design(self,input_arguments) -> "Machine":
        """This creates a new Machine object and returns it
        
        Keyword arguments:
            input_arguments: any
        
        Return Values:
            machine: Machine
        """
        pass
    
class Machine(ABC):
    """ABC for Machine objects"""

    @abstractmethod
    def check_required_properites():
        pass
    
    @abstractmethod
    def get_missing_properties():
        pass

class MachineEvaluator(Evaluator):
    def __init__(self,steps:list('EvaluationStep')):
        self.steps=steps
    
    def evaluate(self,design:Any):
        stateCondition = StateConditions()
        state_in = State(design,stateCondition)
        fullResults = []
        for evalStep in self.steps:
            [results,state_out] = evalStep.step(state_in)
            fullResults.append(deepcopy([state_in,results,state_out]))
            state_in = state_out
        return fullResults

@runtime_checkable
class EvaluationStep(Protocol):
    """Protocol for an evaluation step"""
    @abstractmethod
    def step(self,stateIn:'State')->[Any,'State']:
        pass
    
class StateConditions:
    def __init__(self):
        pass

class State:
    def __init__(self,design:'Design',stateConditions:'StateConditions'):
        self.design = design
        self.stateConditions=stateConditions

class AnalysisStep(EvaluationStep):
    def __init__(self,problemDefinition,analyzer,postAnalyzer):
        self.problemDefinition=problemDefinition
        self.analyzer= analyzer
        self.postAnalyzer=postAnalyzer
    def step(self,stateIn:'State')->[Any,'State']:
        problem=self.problemDefinition.getProblem(stateIn)
        results=self.analyzer.analyze(problem)
        stateOut=self.postAnalyzer.getNextState(results,stateIn)
        return results,stateOut

class ProblemDefinition(Protocol):
    @abstractmethod
    def getProblem(self,state:'State')->'Problem':
        pass

class Problem:
    def __init__(self,machine,op)->'Problem':
        pass
    
class Analyzer(Protocol):
    @abstractmethod
    def analyze(self,problem:'Problem')->Any:
        pass
    
class PostAnalyzer(Protocol):
    @abstractmethod
    def getNextState(self,results:Any,stateIn:'State')->'State':
        pass
        
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MissingValueError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message