# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 09:08:40 2021

@author: Martin Johnson
"""
from typing import Protocol,runtime_checkable,List
from abc import abstractmethod,ABC
import copy 
import pygmo as pg


@runtime_checkable
class EvaluationStep(Protocol):
    """Protocol for an evaluation step"""
    @abstractmethod
    def step(self,stateIn:'State')->['Results','State']:
        pass
    

class AnalysisStep(EvaluationStep):
    def __init__(self,problemDefinition,analyzer,postAnalyzer):
        self.problemDefinition=problemDefinition
        self.analyzer= analyzer
        self.postAnalyzer=postAnalyzer
    def step(self,stateIn:'State')->['Results','State']:
        problem=self.problemDefinition.getProblem(stateIn)
        results=self.analyzer.analyze(problem)
        stateOut=self.postAnalyzer.getNextState(results,stateIn)
        return results,stateOut

class StateUpdateStep:
    def step(self,stateIn:'State')->['Results','State']:
        stateOut=copy.deepcopy(stateIn)
        delattr(stateOut, 'dsl') 
        return [[],stateOut]
    
class StateConditions:
    def __init__(self):
        pass

class State:
    def __init__(self,design:'Design',stateConditions:'StateConditions'):
        self.design = design
        self.stateConditions=stateConditions


class Evaluator:
    def __init__(self,steps:list('EvaluationStep')):
        self.steps=steps
    
    def evaluate(self,design):
        stateCondition = StateConditions()
        state_in = State(design,stateCondition)
        fullResults = []
        for evalStep in self.steps:
            [results,state_out] = evalStep.step(state_in)
            fullResults.append([state_in,results])
            state_in = state_out
        fullResults.append([state_out,[]])
        return fullResults
            
            
class Design:
    def __init__(self,machine,setting):
        self.machine=machine
        self.setting=setting
            
class Results(Protocol):
    analysisType=None
    
class Designer(Protocol):
    @abstractmethod
    def createDesign(self,x)->'Design':
        pass
    
class ProblemDefinition(Protocol):
    @abstractmethod
    def getProblem(self,state:'State')->'Problem':
        pass

class Problem:
    def __init__(self,machine,op)->'Problem':
        pass
    
class Analyzer(Protocol):
    @abstractmethod
    def analyze(self,problem:'Problem')->'Results':
        pass
    
class PostAnalyzer(Protocol):
    @abstractmethod
    def getNextState(self,results:'Results',stateIn:'State')->'State':
        pass
    
class Objective(Protocol):
    @abstractmethod
    def getObjectives(self,fullResults)->'tuple':
        pass
    
    
class MachineDesignProblem:
    def __init__(self,designer:'Designer',
                 evaluator:'Evaluator',objectives:'Objective',dh:'DataHandler',
                 bounds:'tuple',n_obj:'int'):
        self.designer=designer
        self.evaluator=evaluator
        self.objectives=objectives
        self.dh=dh
        self.bounds=bounds
        self.n_obj=n_obj
    def fitness(self,x:'tuple')->'tuple':
        design=self.designer.createDesign(x)
        fullResults=self.evaluator.evaluate(design)
        objs=self.objectives.getObjectives(fullResults)
        self.dh.save(design,fullResults,objs)
        return objs
    def get_bounds(self):
        """Returns bounds for optimization problem""" 
        return self.bounds
    def get_nobj(self):
        """Returns number of objectievs of optimization problem"""
        return self.n_obj 
    
class DataHandler(Protocol):
    @abstractmethod
    def save(self,design:'Design',fullResults,objs):
        pass
    
class Architect(ABC):
    """The architect abc class. This class is the interface between a 
    machine object and the design framework. All the math for calculating an
    Inital Design is done in this object, and a design dictionary is passed
    into the Machine object class on creatation"""
    
    @abstractmethod
    def __init__(self):
        """Initialize the Architect"""
        pass
    
    @abstractmethod
    def create_new_design(self,input_arguments) -> "Machine":
        """This creates a new Machine object and returns it
        
        Keyword arguments:
            input_arguments: any
        
        Return Values:
            machine: Machine
        """
        pass

from abc import ABC, abstractmethod

class Machine(ABC):
    """ABC for Machine objects"""
    @abstractmethod
    def __init__(self):
        pass
        
    @abstractmethod
    def check_required_properites():
        pass
    
    @abstractmethod
    def get_missing_properties():
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

class MachineOptimization:
    def __init__(self,machine_design_problem):
        self.machine_design_problem = machine_design_problem

        
    def run_optimization(self, pop_size, gen_size):
        #######################################################################
        #############                   Create prob object                 ####
        #######################################################################
        
        
        prob = pg.problem(self.machine_design_problem)
        
        #######################################################################
        #############                   Create pop object                 #####
        #######################################################################
        
        
        pop = pg.population(prob,size=pop_size)
        # initial_pop=udp.initial_population(popsize)
        # for ind, chrom in enumerate(initial_pop):
        #     pop.push_back(chrom)
        
        #######################################################################
        #############                   Create algo object                #####
        #######################################################################
        
        algo = pg.algorithm(pg.moead(gen=gen_size, weight_generation="grid",
                                     decomposition="tchebycheff", 
                                     neighbours=20, 
                                     CR=1, F=0.5, eta_m=20, 
                                     realb=0.9, 
                                     limit=2, preserve_diversity=True))
        #######################################################################
        #############                   Run Optimization                  #####
        #######################################################################
        
        pop = algo.evolve(pop)
        
        return pop
