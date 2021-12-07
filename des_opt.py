"""Module holding classes required for design optimization.

This module holds the classes required for optimizing a design using pygmo in MachEval.
"""

import pygmo as pg
import pandas as pd
from typing import Protocol, runtime_checkable, Any
from abc import abstractmethod, ABC
import numpy as np
import pickle


class DesignOptimizationMOEAD:
    def __init__(self, design_problem):
        self.design_problem = design_problem
        self.prob = pg.problem(self.design_problem)

    def initial_pop(self, pop_size):
        pop = pg.population(self.prob, size=pop_size)
        return pop

    def run_optimization(self, pop, gen_size=1, filepath='None'):
        algo = pg.algorithm(pg.moead(gen=2, weight_generation="grid",
                                     decomposition="tchebycheff",
                                     neighbours=20,
                                     CR=1, F=0.5, eta_m=20,
                                     realb=0.9,
                                     limit=2, preserve_diversity=True))
        for i in range(0, gen_size):
            print('This is iteration', i)
            pop = algo.evolve(pop)
            print('Saving current generation')
            self.save_pop(filepath, pop)
        return pop

    #  methods to save and load latest generation for resuming optimization
    def save_pop(self, filepath, pop):
        df = pd.DataFrame(pop.get_x())
        df.to_csv(filepath)

    def load_pop(self, filepath, pop_size):
        try:
            df = pd.read_csv(filepath, index_col=0)
        except FileNotFoundError:
            return None
        pop = pg.population(self.prob)
        for i in range(pop_size):
            print(df.iloc[i])
            pop.push_back(df.iloc[i])
        return pop

class DesignProblem:
    """Class to create, evaluate, and optimize designs

    Attributes:
        designer: Objects which convert free variables to a design.
        evaluator: Objects which evaluate the performance of different designs.
        design_space: Objects which characterizes the design space of the optimization.
        dh: Data handlers which enable saving optimization results and its resumption.
    """
    def __init__(self, designer: 'Designer', evaluator: 'Evaluator', design_space: 'DesignSpace', dh: 'DataHandler'):
        self.__designer = designer
        self.__evaluator = evaluator
        self.__design_space = design_space
        self.__dh = dh
        dh.save_designer(designer)

    def fitness(self, x: 'tuple') -> 'tuple':
        """Calculates the fitness or objectives of each design based on evaluation results.

        This function creates, evaluates, and calculates the fitness of each design generated by the optimization
        algorithm. It also saves the results and handles invalid designs.

        Args:
            x: The list of free variables required to create a complete design

        Returns:
            objs: Returns the fitness of each design

        Raises:
            e: The errors encountered during design creation or evaluation apart from the InvalidDesign error
        """
        try:
            design = self.__designer.create_design(x)
            full_results = self.__evaluator.evaluate(design)
            valid_constraints = self.__design_space.check_constraints(full_results)
            objs = self.__design_space.get_objectives(valid_constraints, full_results)
            self.__dh.save_to_archive(x, design, full_results, objs)
            #print('The fitness values are', objs)
            return objs

        except Exception as e:
            if type(e) is InvalidDesign:
                temp = tuple(map(tuple, 1E4 * np.ones([1, self.get_nobj()])))
                objs = temp[0]
                return objs
                
            ################ Uncomment below block of code to prevent one off errors from JMAG ###################
            # elif type(e) is FileNotFoundError:
            #     print('**********ERROR*************')
            #     temp = tuple(map(tuple, 1E4 * np.ones([1, self.get_nobj()])))
            #     objs = temp[0]
            #     return objs
            else:
                raise e

    def get_bounds(self):
        """Returns bounds for optimization problem"""
        return self.__design_space.bounds

    def get_nobj(self):
        """Returns number of objectives of optimization problem"""
        return self.__design_space.n_obj


@runtime_checkable
class Designer(Protocol):
    """Parent class for all designers

    """
    @abstractmethod
    def create_design(self, x: 'tuple') -> 'Design':
        raise NotImplementedError


class Design(ABC):
    """Parent class for all designs"""
    pass


class Evaluator(Protocol):
    """Parent class for all design evaluators"""
    @abstractmethod
    def evaluate(self, design: 'Design') -> Any:
        pass


class DesignSpace(Protocol):
    """Parent class for a optimization DesignSpace classes"""
    @abstractmethod
    def check_constraints(self, full_results) -> bool:
        raise NotImplementedError

    @abstractmethod
    def n_obj(self) -> int:
        return NotImplementedError

    @abstractmethod
    def get_objectives(self, valid_constraints, full_results) -> tuple:
        raise NotImplementedError

    @abstractmethod
    def bounds(self) -> tuple:
        raise NotImplementedError


class DataHandler(Protocol):
    """Parent class for all data handlers"""
    @abstractmethod
    def save_to_archive(self, x, design, full_results, objs):
        raise NotImplementedError

    @abstractmethod
    def save_designer(self, designer):
        raise NotImplementedError



class OptiData:
    """Object template for serializing optimization results with Pickle"""
    def __init__(self, x, design, full_results, objs):
        self.x = x
        self.design = design
        self.full_results = full_results
        self.objs = objs


class InvalidDesign(Exception):
    """ Exception raised for invalid designs """
    def __init__(self, message='Invalid Design'):
        self.message = message
        super().__init__(self.message)
