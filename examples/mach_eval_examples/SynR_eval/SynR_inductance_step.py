import os
import sys
import copy

from mach_eval import AnalysisStep, ProblemDefinition
from mach_eval.analyzers.electromagnetic import inductance_analyzer as inductance

############################ Define Electromagnetic Step ###########################
class SynR_Ind_ProblemDefinition(ProblemDefinition):
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):

        problem = inductance.Inductance_Problem(
            state.conditions.I_hat, state.conditions.path, state.conditions.study_name, state.conditions.time_step)
        return problem

class SynR_Inductance_PostAnalyzer:
    
    def get_next_state(results, in_state):
        state_out = copy.deepcopy(in_state)

        state_out.conditions.Ld = results["Ld"]
        state_out.conditions.Lq = results["Lq"]
        state_out.conditions.saliency_ratio = results["Ld"]/results["Lq"]

        print("\n************************ INDUCTANCE RESULTS ************************")
        print("Ld = ", state_out.conditions.Ld, " H")
        print("Lq = ", state_out.conditions.Lq, " H")
        print("Saliency Ratio = ", state_out.conditions.saliency_ratio)
        print("*************************************************************************\n")

        return state_out

SynR_inductance_analysis = inductance.Inductance_Analyzer()

SynR_inductance_step = AnalysisStep(SynR_Ind_ProblemDefinition, SynR_inductance_analysis, SynR_Inductance_PostAnalyzer)