import numpy as np
from matplotlib import pyplot as plt
import sys

sys.path.append("..")
import des_opt as mo
import mach_eval as me
import pygmo as pg
from typing import List, Tuple, Any
from copy import deepcopy


class SleeveDesignProblemDefinition(me.ProblemDefinition):
    """Class converts input state into a problem"""

    def get_problem(self, state: 'me.State') -> 'me.Problem':
        """Returns Problem from Input State"""
        # TODO: Define these values from input state
        problem = SleeveDesignProblem(R_sh, sh_mat, R_ri, ri_mat, R_pm, pm_mat, sl_mat)
        return problem


class SleeveDesignProblem:
    """problem class utilized by the Analyzer
    
    Attributes:
        TODO
    """

    def __init__(self, R_sh, sh_mat, R_ri, ri_mat, R_pm, pm_mat, sl_mat, R_st, omega):
        """Creates problem class
        
        Args:
            TODO
            
        """
        self.sh = RotorStructuralComponent(0, R_sh, sh_mat)
        self.ri = RotorStructuralComponent(R_sh, R_ri, ri_mat)
        self.pm = RotorStructuralComponent(R_ri, R_pm, pm_mat)
        self.sl = RotorStructuralComponent(R_pm, None, sl_mat)
        self.R_st = R_st
        self.omega = omega


class RotorStructuralComponent():

    def __init__(self, r_in, r_out, mat):
        self.r_in = r_in
        self.r_out = r_out
        self.mat = mat


class SleeveDesignAnalyzer(me.Analyzer):
    """"Class Analyzes the CubiodProblem  for volume and Surface Areas"""

    def __init__(self):
        self.stressAna = RotorStressAnalyzer()

    def analyze(self, problem: 'me.Problem'):
        """Performs Analysis on a problem

        Args:
            problem (me.Problem): Problem Object

        Returns:
            results (Any): 
                Results of Analysis

        """
        sh = problem.sh
        ri = problem.ri
        pm = problem.pm
        sl = problem.sl
        R_st = problem.R_st
        omega = problem.omega

        max_delta_sl = self.find_min_delta_sl(sh, ri, pm, sl, omega)
        d_sl, delta_sl, stress = self.find_d_sl_and_delta_sl(sh, ri, pm, sl,
                                                             max_delta_sl, R_st)
        results = [d_sl, delta_sl, stress]
        return results

    def find_min_delta_sl(self, sh, ri, pm, sl, omega):
        delta_sl_max = -.001
        delta_sl_vector = np.linspace(0, delta_sl_max, 250)

        ##############################
        # Loop over Undersize Vector
        ##############################
        for i, delta_sl_temp in enumerate(delta_sl_vector):
            sl.delta_sl = delta_sl_temp
            stress = self.stressAna.analyze(sh, ri, pm, sl, omega)
            if stress.sigma_t_sl >= sl.sigmaMaxT:
                max_delta_sl = delta_sl_vector[i - 1]
                break

        return max_delta_sl

    def find_d_sl_and_delta_sl(self, sh, ri, pm, sl, max_delta_sl, R_st):
        delta_sl_vector = np.linspace(max_delta_sl, 0, 25)
        for i, delta_temp in enumerate(delta_sl_vector):
            if i == len(delta_sl_vector) - 1:
                ValidStress = False
                th_final = None
                Dr_final = None
                break
            else:
                sl.set_delta_sl(delta_temp)
                th_vector = np.linspace(.0005, R_st - pm.R_o + delta_temp, 25)
                [d_sl, ValidStress_th] = self.DetermineSleeveThickness(sh, ri, pm, sl, th_vector)
                if ValidStress_th == True:
                    sl.d_sl = d_sl
                    ValidStress = self.stressAna.StressChecks(sh, ri, pm, sl, omega)
                if ValidStress == True:
                    th_final = th
                    Dr_final = Dr_temp
                    break
        print('Sleeve Thickness:', th_final)
        print('Sleeve Undersize:', Dr_final)
        return [th_final, Dr_final]

    def DetermineSleeveThickness(self, sh, ri, pm, sl, th_vector, omega):
        ValidStress = True
        th = 0
        for i, th_temp in enumerate(th_vector):
            sl.set_th(th_temp)
            stress = self.stressAna.analyze(sh, ri, pm, sl, omega)
            if stress.sigma_r_pm <= pm.sigmaMaxR:
                th = th_temp
                break
            else:
                if i == len(th_vector):
                    ValidStress = False
        return [th, ValidStress]


class SleeveDesignPostAnalyzer(me.PostAnalyzer):
    """Converts input state into output state for TemplateAnalyzer"""

    def get_next_state(self, results: Any, stateIn: 'me.State') -> 'me.State':
        stateOut = deepcopy(stateIn)
        # TODO define Post-Analyzer
        return stateOut


class RotorStressProblem:
    """problem class utilized by the Analyzer
    
    Attributes:
        TODO
    """

    def __init__(self, args):
        """Creates problem class
        
        Args:
            TODO
            
        """
        # TODO define problem


class RotorStressAnalyzer(me.Analyzer):
    """"Class Analyzes the CubiodProblem  for volume and Surface Areas"""

    def analyze(self, Problem: 'me.Problem'):
        """Performs Analysis on a problem

        Args:
            problem (me.Problem): Problem Object

        Returns:
            results (Any): 
                Results of Analysis

        """
        # TODO Define Analyzer
        results = []
        return results


if __name__ == '__main__':
    # Create Designer
    settings = None  # TODO define settings
    des = me.MachineDesigner(TemplateArchitect(), settings)

    # Create evaluation steps
    evalSteps = [TemplateConstraintEvaluationStep(),
                 me.AnalysisStep(TemplateProblemDefinition(),
                                 TemplateAnalyzer(),
                                 TemplatePostAnalyzer())]  # TODO define steps
    # Create Evaluator
    evaluator = me.MachineEvaluator(evalSteps)
    objectives = TemplateObjective()
    dh = DataHandler()

    # set evaluation bounds
    bounds = ([0, 0, 0], [1, 1, 1])
    # set number of objectives
    n_obj = 3

    # Create Machine Design Problem
    machDesProb = mo.MachineDesignProblem(des, evaluator, objectives, dh,
                                          bounds, n_obj)

    # Run Optimization
    opt = mo.MachineOptimizationMOEAD(machDesProb)
    pop = opt.run_optimization(496, 10)
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits)
