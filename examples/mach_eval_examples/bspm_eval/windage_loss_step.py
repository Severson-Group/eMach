import os
import sys
from copy import deepcopy
import numpy as np

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"../../..")

from mach_eval.analyzers.mechanical import windage_loss as wl
from mach_eval import AnalysisStep, ProblemDefinition


############################ Define Windage AnalysisStep #####################
class MyWindageProblemDef(ProblemDefinition):
    def get_problem(state):
        design = state.design
        omega = design.settings.speed * 2 * np.pi / 60
        r_ro = design.machine.r_ro + design.machine.d_sl
        l_st = design.machine.l_st
        r_si = design.machine.r_si
        m_dot_air = state.conditions.airflow["Required Airflow"]
        T_air = design.settings.ambient_temp

        prob = wl.WindageLossProblem(omega, r_ro, l_st, r_si, m_dot_air, T_air)
        return prob


class MyWindageLossPostAnalyzer:
    """Converts a State into a problem"""

    def get_next_state(results, in_state):
        state_out = deepcopy(in_state)
        omega = state_out.design.settings.speed * 2 * np.pi / 60
        Pout = state_out.conditions.em["torque_avg"] * omega
        eff = (
            100
            * Pout
            / (
                Pout
                + results[0]
                + results[1]
                + results[2]
                + state_out.conditions.em["copper_loss"]
                + state_out.conditions.em["rotor_iron_loss"]
                + state_out.conditions.em["stator_iron_loss"]
                + state_out.conditions.em["magnet_loss"]
            )
        )
        state_out.conditions.windage = {"loss": results, "efficiency": eff}
        print("\nEfficiency = ", eff[0], " %")
        return state_out


windage_step = AnalysisStep(
    MyWindageProblemDef, wl.WindageLossAnalyzer, MyWindageLossPostAnalyzer
)
