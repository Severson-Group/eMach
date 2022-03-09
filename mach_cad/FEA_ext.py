# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 11:59:14 2021

@author: Martin Johnson
"""
from typing import Protocol
from abc import abstractmethod
from .model_obj import Component
from ..mach_eval import ProblemDefinition, Analyzer, PostAnalyzer
from ..mach_eval import Architect, SettingsHandler


class FEA_Study:
    """FEA_Study is a class which holds all information about an study to be
    preformed in an FEA tool"""

    def __init__(
        self,
        eval_pts: int,
        conditions: list["ConditionBase"],
        settings: list["SettingBase"],
        get_results: list["GetResultBase"],
    ):
        self._eval_pts = eval_pts
        self._conditions = conditions
        self._cond_tokens = []
        self._settings = settings
        self._setting_tokens = []
        self._get_results = get_results
        self._res_tokens = []


class FEA_ProblemDefinition(ProblemDefinition):
    def __init__(self):
        pass

    def get_problem(self, state: "State") -> "FEA_Problem":
        pass


class FEA_Problem:
    """ FEA_Problem contains a set of components and studies to be preformed in 
    an FEA tool"""

    def __init__(self, components: list["Component"], studies: list["FEA_Study"]):
        self._components = components
        self._studies = studies

    @property
    def components(self):
        return self._components

    @property
    def studies(self):
        return self._studies


class FEA_Analyzer(Analyzer):
    """Analyzes FEA_Problems and returns the finished studies"""

    def __init__(self, tool):
        self._tool = tool

    def analyze(self, problem: "FEA_Problem"):

        for comp in problem.components:
            self._tool.make_component(comp)
            # Make each component in the FEA tool

        for study in problem.studies:
            # Loop over each study
            results_dict = dict()
            # Create a results dict to store data
            for get_res in study._get_results:
                results_dict[get_res.name] = [None] * study._eval_pts
                # add the result name to the dictionary and add a empty list of
                # the length of the number of eval points
            for setting in study._settings:
                setting.apply(self._tool)
                # apply the settings to the study
            for ind in range(0, study._eval_pts):
                # for each eval pt in the study
                for cond in study._conditions:
                    cond.apply(self._tool, ind)
                    # Apply condition with its associated value at that point
                tool.run_study()
                # run the study for this eval pt
                for get_res in study._get_results:
                    results_dict[get_res.name][ind] = get_res.extract(self._tool)
                    # extract the requested result at this eval point and save
                for cond in study._conditions:
                    cond.unapply(self._tool, ind)
                    # unapply the condition to return to the inital state
            study.results = results_dict
            # store the results to the study

        return problem._studies
        # return the completed studies


class FEA_PostAnalyzer(PostAnalyzer):
    def __init__(self):
        pass

    def get_next_state(self, results: Any, state_in: "State") -> "State":
        pass


class ConditionBase(Protocol):
    """Conditions are actions or states applied at each eval point in a 
    FEA tool"""

    @abstractmethod
    def apply(self, tool, ind):
        """Apply the conditon at this index"""
        raise NotImplementedError

    @abstractmethod
    def unapply(self, tool, ind):
        """Unapply the conditon at this index"""
        raise NotImplementedError


class SettingBase(Protocol):
    """Settings are actions or states applied once per study"""

    @abstractmethod
    def apply(self, tool):
        """ Apply the setting in the tool"""
        raise NotImplementedError


class GetResultBase(Protocol):
    """GetResults define an extraction process in a FEA tool"""

    @abstractmethod
    def extract(self, tool):
        raise NotImplementedError

    @abstractmethod
    @property
    def name(self):
        raise NotImplementedError

