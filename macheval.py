# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:54:48 2021

@author: Martin Johnson
"""

from typing import Protocol,runtime_checkable,Any
from abc import abstractmethod,ABC
from mach_opt import EvaluationStep,State,Design




class MachineDesign(Design):
    def __init__(self,machine:'Machine',setting: Any):
        self.machine=machine
        self.setting=setting     
        
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