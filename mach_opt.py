# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:43:59 2021

@author: Martin Johnson
"""
import pygmo as pg
from typing import Protocol,runtime_checkable,Any
from abc import abstractmethod,ABC


class MachineOptimizationMOEAD:
    def __init__(self,machine_design_problem):
        self.machine_design_problem = machine_design_problem

        
    def run_optimization(self, pop_size, gen_size):
        prob = pg.problem(self.machine_design_problem)
        pop = pg.population(prob,size=pop_size)
        algo = pg.algorithm(pg.moead(gen=gen_size, weight_generation="grid",
                                     decomposition="tchebycheff", 
                                     neighbours=20, 
                                     CR=1, F=0.5, eta_m=20, 
                                     realb=0.9, 
                                     limit=2, preserve_diversity=True))
        pop = algo.evolve(pop)
        return pop

    
class MachineDesignProblem:
    def __init__(self,designer:'Designer',
                 evaluator:'Evaluator', objectives:'Objective',
                 dh:'DataHandler', bounds:'tuple', n_obj:'int'):
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

class Designer(Protocol):
    @abstractmethod
    def createDesign(self,x:'tuple')->'Design':
        raise NotImplementedError
        
class Design(ABC):
    pass

        
class Evaluator:
    def __init__(self,steps:list('EvaluationStep')):
        self.steps=steps
    
    def evaluate(self,design:Any):
        stateCondition = StateConditions()
        state_in = State(design,stateCondition)
        fullResults = []
        for evalStep in self.steps:
            [results,state_out] = evalStep.step(state_in)
            fullResults.append([state_in,results])
            state_in = state_out
        fullResults.append([state_out,[]])
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


class Objective(Protocol):
    @abstractmethod
    def getObjectives(self,fullResults)->'tuple':
        raise NotImplementedError
        

class DataHandler(Protocol):
    @abstractmethod
    def save(self,design:'Design',fullResults,objs):
        raise NotImplementedError