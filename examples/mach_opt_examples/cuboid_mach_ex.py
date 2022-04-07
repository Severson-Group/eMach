import os
import sys
# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import numpy as np
from matplotlib import pyplot as plt
from typing import Any, List

import mach_opt as mo
import mach_eval as me
import pygmo as pg
from copy import deepcopy


class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class CubiodArchitect(me.Architect):
    """Class converts input tuple x into a Cubiod object"""

    def create_new_design(self, x: tuple) -> "Cubiod":
        """
        converts x tuple into a Cubiod object.

        Args:
            x (tuple): Input free variables.
            
        Returns:
            cubiod (Cubiod): Cubiod object
        """

        L = x[0]
        W = x[1]
        H = x[2]
        cubiod = Cubiod(L, W, H)
        return cubiod


class Cubiod(me.Machine):
    """Class defines a cubiod object of Length and width
    
    Attributes:
        L (float): Length of Cubiod.
        W (float): Width of Cubiod.
        H (float); Height of Cubiod
    """

    def __init__(self, L: float, W: float, H: float):
        """Creates Cubiod object.

        Args:
            L (float): Length of Cubiod
            W (float): Width of Cubiod

        """
        self.L = L
        self.W = W
        self.H = H

    def check_required_properites():
        pass

    def get_missing_properties():
        pass


class CubiodProblemDefinition(me.ProblemDefinition):
    """Class converts input state into a CubiodProblem"""

    def getProblem(self, state: "me.State") -> "CubiodProblem":
        """Returns CubiodProblem from Input State"""
        problem = CubiodProblem(state.design.machine)
        return problem


class CubiodProblem:
    """problem class utilized by the CubiodAnalyzer"""

    def __init__(self, cubiod: "Cubiod"):
        self.W = cubiod.W
        self.H = cubiod.H
        self.L = cubiod.L


class CubiodAnalyzer(me.Analyzer):
    """"Class Analyzes the CubiodProblem  for volume and Surface Areas"""

    def analyze(self, cubiodProblem: "CubiodProblem"):
        """calculates area and perimeter of cubiod

        Args:
            cubiodProblem (CubiodProblem): problem Object

        Returns:
            [V,SA,total,SA_Lateral] (List[float,float,float]): 
                Volume and total/lateral surface area of cubiod

        """
        V = cubiodProblem.L * cubiodProblem.W * cubiodProblem.H
        SA_total = (
            2 * cubiodProblem.L * cubiodProblem.W
            + 2 * cubiodProblem.W * cubiodProblem.H
            + 2 * cubiodProblem.L * cubiodProblem.H
        )
        SA_Lateral = (
            2 * cubiodProblem.W * cubiodProblem.H
            + 2 * cubiodProblem.L * cubiodProblem.H
        )
        return [V, SA_total, SA_Lateral]


class CubiodPostAnalyzer(me.PostAnalyzer):
    """Converts input state into output state for Cubiod Analyzer"""

    def getNextState(self, results: Any, stateIn: "me.State") -> "me.State":
        stateOut = deepcopy(stateIn)
        stateOut.stateConditions.V = results[0]
        stateOut.stateConditions.SA_Total = results[1]
        stateOut.stateConditions.SA_Lateral = results[2]
        return stateOut


class ConstraintProblemDefinition(me.ProblemDefinition):
    """Converts Input State to ConstraintProblem"""

    def getProblem(self, state: "me.State") -> "CubiodProblem":
        """Converts Input State to ConstraintProblem"""
        problem = ConstraintProblem(state.design.machine, state.design.setting)
        return problem


class ConstraintProblem:
    def __init__(self, cubiod: "Cubiod", weight):
        self.W = cubiod.W
        self.H = cubiod.H
        self.L = cubiod.L
        self.weight = weight


class ConstraintAnalyzer(me.Analyzer):
    """"Class evaluates the cubiod object for volume and Surface Areas"""

    def analyze(self, problem: "ConstraintProblem"):

        value = problem.W + problem.L + 0.1 * problem.H - problem.weight
        if value >= 0:
            raise ConstraintError(value)
        else:
            return value


class ConstraintError(Error):
    def __init__(self, value):
        self.value = value


class ConstraintPostAnalyzer(me.PostAnalyzer):
    def getNextState(self, results: Any, stateIn: "me.State") -> "me.State":
        stateOut = deepcopy(stateIn)
        stateOut.stateConditions.constraintValue = results
        return stateOut


class ConstraintEvaluationStep(me.EvaluationStep):
    def step(self, stateIn):
        cubiod = stateIn.design.machine
        weight = stateIn.design.setting
        value = cubiod.W ** 0.5 + cubiod.L ** 2.2 + 0.1 * cubiod.H - weight
        if value >= 0:
            raise ConstraintError(value)
        else:
            stateOut = deepcopy(stateIn)
            stateOut.stateConditions.constraintValue = value
            return [value, stateOut]


class Cubiomobj:
    """Class defines objectives of cubiod optimization"""

    def getObjectives(self, results: "List[float,float]"):
        """ Calculates objectives from evaluation results
        

        Args:
            results (List(float,float)): Results from CubiodEval

        Returns:
            Tuple[float,float]: Minimize volume, Maximize Total Surface Area,
                                Minimize Lateral Surface area
        """
        final_state = results[-1][-1]
        V = final_state.stateConditions.V
        SA_Total = final_state.stateConditions.SA_Total
        SA_Lateral = final_state.stateConditions.SA_Lateral
        return (V, -SA_Total, SA_Lateral)


class DataHandler:
    def save(self, design, fullResults, objs):
        """Unimplented data handler"""
        pass


if __name__ == "__main__":
    weight = 5
    des = me.MachineDesigner(CubiodArchitect(), weight)
    # evalSteps=[me.AnalysisStep(ConstraintProblemDefinition(),
    #                            ConstraintAnalyzer(),
    #                            ConstraintPostAnalyzer()),
    #            me.AnalysisStep(CubiodProblemDefinition(),
    #                            CubiodAnalyzer(),
    #                            CubiodPostAnalyzer())]
    evalSteps = [
        ConstraintEvaluationStep(),
        me.AnalysisStep(
            CubiodProblemDefinition(), CubiodAnalyzer(), CubiodPostAnalyzer()
        ),
    ]
    evaluator = me.MachineEvaluator(evalSteps)
    objectives = Cubiomobj()
    dh = DataHandler()
    bounds = ([0.5, 0.1, 0.25], [10, 3, 5])
    n_obj = 3
    machDesProb = mo.DesignProblem(des, evaluator, objectives, dh, bounds, n_obj)
    opt = mo.DesignOptimizationMOEAD(machDesProb)
    pop = opt.run_optimization(496, 10)
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_mominated_sorting(fits)

    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    im1 = ax1.scatter(fits[ndf[0], 0], fits[ndf[0], 1], c=fits[ndf[0], 2], marker="x")
    ax1.set_xlabel("Volume")
    ax1.set_ylabel("Total Surface Area")
    ax1.set_title("Pareto Front")
    cb1 = fig1.colorbar(im1, ax=ax1,)
    cb1.set_label("Lateral Surface Area")

    fig2 = plt.figure()
    ax2 = fig2.add_subplot()
    im2 = ax2.scatter(fits[ndf[0], 1], fits[ndf[0], 2], c=fits[ndf[0], 0], marker="x")
    ax2.set_xlabel("Total Surface Area")
    ax2.set_ylabel("Lateral Surface Area")
    ax2.set_title("Pareto Front")
    cb2 = fig2.colorbar(im2, ax=ax2,)
    cb2.set_label("Volume")

    fig3 = plt.figure()
    ax3 = fig3.add_subplot()
    im3 = ax3.scatter(fits[ndf[0], 2], fits[ndf[0], 0], c=fits[ndf[0], 1], marker="x")
    ax3.set_xlabel("Lateral Surface Area")
    ax3.set_ylabel("Volume")
    ax3.set_title("Pareto Front")
    cb3 = fig3.colorbar(im3, ax=ax3,)
    cb3.set_label("Total Surface Area")

