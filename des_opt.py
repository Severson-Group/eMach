
import pygmo as pg
from typing import Protocol, runtime_checkable, Any
from abc import abstractmethod, ABC
import numpy as np
import traceback


class DesignOptimizationMOEAD:
    def __init__(self, design_problem):
        self.design_problem = design_problem
        self.prob = pg.problem(self.design_problem)

    def initial_pop(self, pop_size):
        pop = pg.population(self.prob, size=pop_size)
        return pop

    def run_optimization(self, pop, gen_size):
        algo = pg.algorithm(pg.moead(gen=1, weight_generation="grid",
                                     decomposition="tchebycheff",
                                     neighbours=20,
                                     CR=1, F=0.5, eta_m=20,
                                     realb=0.9,
                                     limit=2, preserve_diversity=True))
        for _ in range(0, gen_size):
            pop = algo.evolve(pop)
        return pop




class DesignProblem:
    def __init__(self, designer: 'Designer', evaluator: 'Evaluator', optimization: 'Optimization', dh: 'DataHandler'):
        self.designer = designer
        self.evaluator = evaluator
        self.optimization = optimization
        self.dh = dh

    def fitness(self, x: 'tuple') -> 'tuple':
        try:
            design = self.designer.create_design(x)
            full_results = self.evaluator.evaluate(design)
            valid_constraints = self.optimization.check_constraints(full_results)
            objs = self.optimization.get_objectives(valid_constraints, full_results)
            self.dh.save(design, full_results, objs)
        except Exception as e:
            # print(e)
            # print(traceback.format_exc())
            if e is InvalidDesign:
                temp = tuple(map(tuple, 1E10 * np.ones([1, self.get_nobj()])))
                objs = temp[0]
                return objs
            else:
                raise e


    def get_bounds(self):
        """Returns bounds for optimization problem"""
        bounds_denorm = self.optimization.bounds
        print('---------------------\nBounds:')
        for idx, bounds in enumerate(bounds_denorm):
            print(idx, bounds)
        min_b, max_b = np.asarray(bounds_denorm).T
        min_b, max_b = min_b.astype(float), max_b.astype(float)
        return min_b.tolist(), max_b.tolist()

    def get_nobj(self):
        """Returns number of objectives of optimization problem"""
        return self.optimization.n_obj


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


class Optimization(Protocol):
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
    def get_bounds(self, x) -> tuple:
        raise NotImplementedError


class DataHandler(Protocol):
    @abstractmethod
    def save(self, design: 'Design', full_results, objs):
        raise NotImplementedError


class InvalidDesign(Exception):
    """ Exception raised for invalid designs """
    def __init__(self, message = 'Invalid Design'):
        self.message = message
        super().__init__(self.message)