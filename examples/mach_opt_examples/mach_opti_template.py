import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

import mach_opt as mo
import mach_eval as me
import pygmo as pg
from typing import List, Tuple, Any
from copy import deepcopy


class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class TemplateArchitect(me.Architect):
    """Class converts input tuple x into a machine object"""

    def create_new_design(self, x: Tuple) -> "me.Machine":
        """
        converts x tuple into a machine object.

        Args:
            x (tuple): Input free variables.
            
        Returns:
            machine (me.Machine): Machine object
        """

        # TOmo Define Architect
        machine = TemplateMachine()
        return machine


class TemplateSettingsHanlder(me.SettingsHandler):
    """Settings hanlder for design creation"""

    def getSettings(self, x):
        settings = NotImplementedError
        return settings


class TemplateMachine(me.Machine):
    """Class defines a Machine object 
    
    Attributes:
        TOmo
    """

    def __init__(self):
        """Creates a machine object.

        Args:
            TOmo

        """

        # TOmo Define Machine

    def check_required_properites():
        """Checks for required input properties"""
        # TOmo
        pass

    def get_missing_properties():
        """Returns missing input properites"""
        # TOmo
        pass


class TemplateProblemDefinition(me.ProblemDefinition):
    """Class converts input state into a problem"""

    def getProblem(self, state: "me.State") -> "me.Problem":
        """Returns Problem from Input State"""
        # TOmo define problem definition
        args = None
        problem = TemplateProblem(args)
        return problem


class TemplateProblem:
    """problem class utilized by the Analyzer
    
    Attributes:
        TOmo
    """

    def __init__(self, args):
        """Creates problem class
        
        Args:
            TOmo
            
        """
        # TOmo define problem


class TemplateAnalyzer(me.Analyzer):
    """"Class Analyzes the CubiodProblem  for volume and Surface Areas"""

    def analyze(self, problem: "me.Problem"):
        """Performs Analysis on a problem

        Args:
            problem (me.Problem): Problem Object

        Returns:
            results (Any): 
                Results of Analysis

        """
        # TOmo Define Analyzer
        results = []
        return results


class TemplatePostAnalyzer(me.PostAnalyzer):
    """Converts input state into output state for TemplateAnalyzer"""

    def getNextState(self, results: Any, stateIn: "me.State") -> "me.State":
        stateOut = deepcopy(stateIn)
        # TOmo define Post-Analyzer
        return stateOut


class ConstraintError(Error):
    """Error for violating optimization constraint"""

    def __init__(self, value):
        # TOmo define error
        self.value = value


class TemplateConstraintEvaluationStep(me.EvaluationStep):
    """Constraint evaluation step template"""

    def step(self, stateIn):
        """Checks input state to see if constraint is violated
        
        Raises ConstraintError if violated, otherwise appends values to 
        State conditions and moves forward"""

        value = None  # TOmo define constraint
        if value >= 0:
            raise ConstraintError(value)
        else:
            stateOut = deepcopy(stateIn)
            stateOut.stateConditions.constraintValue = value
            return [value, stateOut]


class TemplateObjective:
    """Class defines objectives of cubiod optimization"""

    def getObjectives(self, results: "List[float,float]"):
        """ Calculates objectives from evaluation results
        

        Args:
            results (List): Results from MachineEvaluator

        Returns:
            Tuple: objectives tuple 
        """
        final_state = results[-1][-1]
        results = None  # TO DO define objectives
        return results


class DataHandler:
    def save(self, design, fullResults, objs):
        """Unimplented data handler"""
        # TOmo Define datahandler
        pass


if __name__ == "__main__":

    # Create Designer
    des = me.MachineDesigner(TemplateArchitect(), TemplateSettingsHanlder())

    # Create evaluation steps
    evalSteps = [
        TemplateConstraintEvaluationStep(),
        me.AnalysisStep(
            TemplateProblemDefinition(), TemplateAnalyzer(), TemplatePostAnalyzer()
        ),
    ]  # TOmo define steps
    # Create Evaluator
    evaluator = me.MachineEvaluator(evalSteps)
    objectives = TemplateObjective()
    dh = DataHandler()

    # set evaluation bounds
    bounds = ([0, 0, 0], [1, 1, 1])
    # set number of objectives
    n_obj = 3

    # Create Machine Design Problem
    machDesProb = mo.DesignProblem(des, evaluator, objectives, dh, bounds, n_obj)

    # Run Optimization
    opt = mo.DesignOptimizationMOEAD(machDesProb)
    pop = opt.run_optimization(496, 10)
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_mominated_sorting(fits)

