import pygmo as pg
from typing import Protocol, runtime_checkable, Any
from abc import abstractmethod, ABC
import numpy as np
import traceback


class DesignOptimizationMOEAD:
    def __init__(self, machine_design_problem):
        self.machine_design_problem = machine_design_problem

    def run_optimization(self, pop_size, gen_size):
        prob = pg.problem(self.machine_design_problem)
        pop = pg.population(prob, size=pop_size)
        algo = pg.algorithm(pg.moead(gen=gen_size, weight_generation="grid",
                                     decomposition="tchebycheff",
                                     neighbours=20,
                                     CR=1, F=0.5, eta_m=20,
                                     realb=0.9,
                                     limit=2, preserve_diversity=True))
        pop = algo.evolve(pop)
        return pop


class DesignProblem:
    def __init__(self, designer: 'Designer', evaluator: 'Evaluator', constraints: 'Constraint', objectives: 'Objective'
                 , dh: 'DataHandler', bounds: 'tuple', n_obj: 'int'):
        self.designer = designer
        self.evaluator = evaluator
        self.constraints = constraints
        self.objectives = objectives
        self.dh = dh
        self.bounds = bounds
        self.n_obj = n_obj

    def fitness(self, x: 'tuple') -> 'tuple':
        try:
            design = self.designer.create_design(x)
            full_results = self.evaluator.evaluate(design)
            valid_constraints = self.constraints.check_constraints(full_results)
            objs = self.objectives.get_objectives(valid_constraints, full_results)
            self.dh.save(design, full_results, objs)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            temp = tuple(map(tuple, 1E10 * np.ones([1, self.get_nobj()])))
            objs = temp[0]
        return objs

    def get_bounds(self):
        """Returns bounds for optimization problem"""
        return self.bounds

    def get_nobj(self):
        """Returns number of objectives of optimization problem"""
        return self.n_obj


@runtime_checkable
class Designer(Protocol):
    @abstractmethod
    def create_design(self, x: 'tuple') -> 'Design':
        raise NotImplementedError


class Design(ABC):
    pass


class Evaluator(Protocol):
    @abstractmethod
    def evaluate(self, design: 'Design') -> Any:
        pass


class Constraint(Protocol):
    @abstractmethod
    def check_constraints(self, full_results) -> bool:
        raise NotImplementedError


class Objective(Protocol):
    @abstractmethod
    def get_objectives(self, valid_constraints, full_results) -> tuple:
        raise NotImplementedError


class DataHandler(Protocol):
    @abstractmethod
    def save(self, design: 'Design', full_results, objs):
        raise NotImplementedError
