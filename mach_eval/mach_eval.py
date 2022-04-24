"""Module holding base classes required for machine evaluation.

This module holds the parent classes required for machine evaluation. The module structure has been constructed in
manner suitable for both machine optimization and evaluation.
"""

from typing import Protocol, runtime_checkable, Any, List
from abc import abstractmethod, ABC
import sys
sys.path.append("..")
from .. import mach_opt as mo
from copy import deepcopy

__all__ = [
    "MachineDesign",
    "MachineDesigner",
    "SettingsHandler",
    "Architect",
    "Machine",
    "MachineEvaluator",
    "EvaluationStep",
    "Conditions",
    "State",
    "AnalysisStep",
    "ProblemDefinition",
    "Problem",
    "Analyzer",
    "PostAnalyzer",
]


class MachineDesign(mo.Design):
    """Class representing a complete machine design, includes machine physical description and operating conditions.

    Attributes:
        machine: Holds information on machine dimensions, materials, and nameplate specs
        
        settings: Operating conditions of machine. Can include speed, current, expected power / torque etc.
    """

    def __init__(self, machine: "Machine", settings: Any):
        self.machine = machine
        self.settings = settings


class MachineDesigner(mo.Designer):
    """Class representing a machine designer.

    Attributes:
        arch: Class which converts optimization free variables to a complete set of machine dimensions required to
        fully define a machine.
        
        settings_handler: Class which converts optimization free variable to machine operating conditions.
    """

    def __init__(self, arch: "Architect", settings_handler: "SettingsHandler"):
        self.arch = arch
        self.settings_handler = settings_handler

    def create_design(self, x: "tuple") -> "Design":
        """Creates a machine design from free variables.

        Args:
            x: Tuple of design free variables. Should be defined in a particular sequence based on arch and settings_handler
        Returns:
            A complete machine design including machine physical description and operating conditions.
        """
        machine = self.arch.create_new_design(x)
        settings = self.settings_handler.get_settings(x)
        design = MachineDesign(machine, settings)
        return design


class SettingsHandler(Protocol):
    @abstractmethod
    def get_settings(self, x: "tuple"):
        raise NotImplementedError


class Architect(Protocol):
    """Base class for all machine design creating architect classes.

    Child classes of Architect establish the interface between a machine object and the design framework. All the math
    for calculating an initial machine design is done within child classes of this class, and a design dictionary is
    passed into the Machine object class on creation.
    """

    @abstractmethod
    def create_new_design(self, input_arguments: Any) -> "Machine":
        """Creates a new Machine object and returns it
        
        Args:
            input_arguments: Any
        
        Returns:
            machine: Machine
        """
        pass


class Machine(ABC):
    """Abstract base class for Machine objects"""

    # @abstractmethod
    # def check_required_properties(self):
    #     pass

    # @abstractmethod
    # def get_missing_properties(self):
    #     pass


class MachineEvaluator(mo.Evaluator):
    """Wrapper class for all steps involved in analyzing a MachineDesign

    Attributes:
        steps: Sequential list of steps involved in evaluating a MachineDesign
    """

    def __init__(self, steps: List["EvaluationStep"]):
        self.steps = steps

    def evaluate(self, design: Any):
        """Evaluates a MachineDesign

        Evaluates a MachineDesign with the list of evaluation steps that the class object was initialized with

        Args:
            design: MachineDesign object to be evaluated
        Returns:
            full_results: List of results obtained from each evaluation step
        """
        state_condition = Conditions()
        state_in = State(design, state_condition)
        full_results = []
        for evalStep in self.steps:
            [results, state_out] = evalStep.step(state_in)
            full_results.append(deepcopy([state_in, results, state_out]))
            state_in = state_out
        return full_results


@runtime_checkable
class EvaluationStep(Protocol):
    """Protocol for an evaluation step"""

    @abstractmethod
    def step(self, state_in: "State") -> [Any, "State"]:
        pass


class Conditions:
    """Class to hold state conditions during machine evaluation.

    This is a dummy class whose purpose is hold attributes required by subsequent steps involved in evaluating a machine
    design.
    """

    def __init__(self):
        pass


class State:
    """Class to hold the state of machine evaluation over each evaluation step.

    The purpose of this class is to hold the Machine object and conditions required for subsequent steps involved in
    evaluating a machine design.

    Attributes:
        design: machine design used by the next step
        conditions: additional information required for subsequent evaluation steps
    """

    def __init__(self, design: "Design", conditions: "Conditions"):
        self.design = design
        self.conditions = conditions


class AnalysisStep(EvaluationStep):
    """Class representing a step which involves detailed analysis.

    Attributes:
        problem_definition: class or object defining the problem to be analyzed. This attribute acts as the interface between the machine design and the analyzer.
        
        analyzer: class or object which evaluates any aspect of a machine design.
        
        post_analyzer: class or object which processes the results obtained from the analyzer and packages in a form suitable for subsequent steps.
    """

    def __init__(self, problem_definition, analyzer, post_analyzer):
        self.problem_definition = problem_definition
        self.analyzer = analyzer
        self.post_analyzer = post_analyzer

    def step(self, state_in: "State") -> [Any, "State"]:
        """Method to evaluate design using a analyzer

        Args:
            state_in: input state which is to be evaluated.
        Returns:
            results: Results obtained from the analyzer.
            
            state_out: Output state to be used by the next step involved in the machine design evaluation.
        """
        problem = self.problem_definition.get_problem(state_in)
        results = self.analyzer.analyze(problem)
        state_out = self.post_analyzer.get_next_state(results, state_in)
        return results, state_out


class ProblemDefinition(Protocol):
    """Protocol for a problem definition"""

    @abstractmethod
    def get_problem(self, state: "State") -> "Problem":
        pass


class Problem:
    def __init__(self, machine, op):
        pass


class Analyzer(Protocol):
    """Protocol for an analyzer"""

    @abstractmethod
    def analyze(self, problem: "Problem") -> Any:
        pass


class PostAnalyzer(Protocol):
    """Protocol for a post analyzer """

    @abstractmethod
    def get_next_state(self, results: Any, state_in: "State") -> "State":
        pass


# class Error(Exception):
#     """Base class for exceptions in this module."""

#     pass


# class MissingValueError(Error):
#     """Exception raised for errors in the input.

#     Attributes:
#         expression: input expression in which the error occurred

#         message: explanation of the error
#     """

#     def __init__(self, expression, message):
#         self.expression = expression
#         self.message = message
