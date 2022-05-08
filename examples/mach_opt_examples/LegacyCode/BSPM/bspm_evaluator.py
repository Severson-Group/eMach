import os
import sys
from copy import deepcopy
import numpy as np

os.chdir(os.path.dirname(__file__))
sys.path.append("../../../..")


from local_analyzers.em import BSPM_EM_Analysis
from mach_eval.analyzers import structrual_analyzer as stra
from mach_eval.analyzers import thermal_analyzer as therm
from mach_eval.analyzers import thermal_stator as st_therm
from specifications.analyzer_config.em_fea_config import JMAG_FEA_Configuration

from problems.bspm_em_problem import BSPM_EM_Problem
from post_analyzers.bpsm_em_post_analyzer import BSPM_EM_PostAnalyzer
from length_scale_step import LengthScaleStep
from mach_eval import AnalysisStep, MachineEvaluator

from mach_opt import InvalidDesign


############################ Define Struct AnalysisStep ######################
stress_limits = {
    "rad_sleeve": -100e6,
    "tan_sleeve": 1300e6,
    "rad_magnets": 0,
    "tan_magnets": 80e6,
}
# spd = sta.SleeveProblemDef(design_variant)
# problem = spd.get_problem()
struct_ana = stra.SleeveAnalyzer(stress_limits)


class MySleeveProblemDef:
    def get_problem(state):
        design = state.design
        material_dict = {}
        for key, value in design.machine.rotor_iron_mat.items():
            material_dict[key] = value
        for key, value in design.machine.magnet_mat.items():
            material_dict[key] = value
        for key, value in design.machine.rotor_sleeve_mat.items():
            material_dict[key] = value
        for key, value in design.machine.shaft_mat.items():
            material_dict[key] = value

        material_dict["alpha_sh"] = 1.2e-5
        material_dict["alpha_rc"] = 1.2e-5
        material_dict["alpha_pm"] = 5e-6
        material_dict["alpha_sl_t"] = -4.7e-7
        material_dict["alpha_sl_r"] = 0.3e-6

        r_sh = design.machine.r_sh
        r_ro = design.machine.r_ro
        d_m = design.machine.d_m
        N = design.settings.speed
        deltaT = design.settings.rotor_temp_rise

        problem = stra.SleeveProblem(r_sh, d_m, r_ro, deltaT, material_dict, N)
        return problem


class MyStructPostAnalyzer:
    """Converts a State into a problem"""

    def get_next_state(results, in_state):
        if results is False:
            raise InvalidDesign("Suitable sleeve not found")
        else:
            print("Results are ", type(results))
            machine = in_state.design.machine
            new_machine = machine.clone(machine_parameter_dict={"d_sl": results[0]})
        state_out = deepcopy(in_state)
        state_out.design.machine = new_machine
        return state_out


struct_step = AnalysisStep(MySleeveProblemDef, struct_ana, MyStructPostAnalyzer)

############################ Define EMAnalysisStep ###########################
class BSPM_EM_ProblemDefinition:
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):
        problem = BSPM_EM_Problem(state.design.machine, state.design.settings)
        return problem


# initialize em analyzer class with FEA configuration
em_analysis = BSPM_EM_Analysis(JMAG_FEA_Configuration)
# define AnalysysStep for EM evaluation
em_step = AnalysisStep(BSPM_EM_ProblemDefinition, em_analysis, BSPM_EM_PostAnalyzer)

###################### Define Rotor Thermal AnalysisStep #####################
class MyAirflowProblemDef:
    def get_problem(state):
        design = state.design
        material_dict = {}
        for key, value in design.machine.rotor_iron_mat.items():
            material_dict[key] = value
        for key, value in design.machine.magnet_mat.items():
            material_dict[key] = value
        for key, value in design.machine.rotor_sleeve_mat.items():
            material_dict[key] = value
        for key, value in design.machine.shaft_mat.items():
            material_dict[key] = value
        for key, value in design.machine.air_mat.items():
            material_dict[key] = value
        for key, value in design.machine.rotor_hub.items():
            material_dict[key] = value

        material_dict["alpha_sh"] = 1.2e-5
        material_dict["alpha_rc"] = 1.2e-5
        material_dict["alpha_pm"] = 5e-6
        material_dict["alpha_sl_t"] = -4.7e-7
        material_dict["alpha_sl_r"] = 0.3e-6

        r_sh = design.machine.r_sh
        d_ri = design.machine.d_ri
        r_ro = design.machine.r_ro
        d_sl = design.machine.d_sl
        r_si = design.machine.r_si
        l_st = design.machine.l_st
        l_hub = 3e-3
        T_ref = design.settings.ambient_temp
        omega = design.settings.speed * 2 * np.pi / 60
        losses = state.conditions.em

        rotor_max_temp = material_dict["magnet_max_temperature"]

        prob = therm.AirflowProblem(
            r_sh,
            d_ri,
            r_ro,
            d_sl,
            r_si,
            l_st,
            l_hub,
            T_ref,
            losses,
            omega,
            rotor_max_temp,
            material_dict,
        )
        return prob


class MyAirflowPostAnalyzer:
    """Converts a State into a problem"""

    def get_next_state(results, in_state):
        if results["valid"] is False:
            raise InvalidDesign("Magnet temperature beyond limits")
        else:
            state_out = deepcopy(in_state)
            state_out.conditions.airflow = results
        return state_out


rotor_thermal_step = AnalysisStep(
    MyAirflowProblemDef, therm.AirflowAnalyzer, MyAirflowPostAnalyzer
)

###################### Define Stator Thermal AnalysisStep #####################
class MyThermalProblemDefinition:
    """Class converts input state into a problem"""

    def get_problem(state):
        """Returns Problem from Input State"""
        # TODO define problem definition
        g_sy = state.conditions.g_sy  # Volumetric loss in Stator Yoke [W/m^3]
        g_th = state.conditions.g_th  # Volumetric loss in Stator Tooth [W/m^3]
        w_st = state.design.machine.w_st  # Tooth width [m]
        l_st = state.design.machine.l_st  # Stack length [m]
        r_sy = state.design.machine.r_so - state.design.machine.d_sy
        l_tooth = r_sy - state.design.machine.r_si  # Tooth length r_sy-r_si [m]
        alpha_q = 2 * np.pi / state.design.machine.Q  # [rad]
        r_so = state.design.machine.r_so  # outer stator radius [m]

        k_ins = 1  # thermal insulation conductivity (~1)
        w_ins = 0.5e-3  # insulation thickness [m] (.5mm)
        k_fe = state.design.machine.stator_iron_mat["core_therm_conductivity"]
        h = 100  # convection co-eff W/m^2K
        alpha_slot = alpha_q - 2 * np.arctan(
            w_st / (2 * r_sy)
        )  # span of back of stator slot [rad]
        T_coil_max = 150  # Max rise in coil temp [K]

        r_si = state.design.machine.r_si  # inner stator radius
        Q_coil = state.conditions.Q_coil  # ohmic loss per coil
        h_slot = 0  # in slot convection coeff [W/m^2K] set to 0

        problem = st_therm.ThermalProblem(
            g_sy,
            g_th,
            w_st,
            l_st,
            l_tooth,
            alpha_q,
            r_so,
            r_sy,
            k_ins,
            w_ins,
            k_fe,
            h,
            alpha_slot,
            T_coil_max,
            r_si,
            Q_coil,
            h_slot,
        )
        return problem


class MyStatorThermalPostAnalyzer:
    """Converts input state into output state for TemplateAnalyzer"""

    def get_next_state(results, stateIn):
        if results[5] is False:
            raise InvalidDesign("Magnet temperature beyond limits")
        else:
            stateOut = deepcopy(stateIn)
            stateOut.conditions.T_coil = results[0]
            stateOut.conditions.T_sy = results[1]
            stateOut.conditions.Q_coil = results[2]
            stateOut.conditions.Q_yoke = results[3]
            stateOut.conditions.Q_tooth = results[4]

        print("Coil Temp is ", results[0])
        print("Stator Temp is ", results[1])
        return stateOut


stator_therm_step = AnalysisStep(
    MyThermalProblemDefinition, st_therm.ThermalAnalyzer, MyStatorThermalPostAnalyzer,
)

############################ Define Windage AnalysisStep #####################
class MyWindageProblemDef:
    def get_problem(state):
        design = state.design
        omega = design.settings.speed * 2 * np.pi / 60
        r_ro = design.machine.r_ro + design.machine.d_sl
        l_st = design.machine.l_st
        r_si = design.machine.r_si
        airgap = design.machine.delta
        m_dot_air = state.conditions.airflow["Required Airflow"]
        T_air = design.settings.ambient_temp

        prob = therm.WindageProblem(omega, r_ro, l_st, r_si, airgap, m_dot_air, T_air)
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
                + results
                + state_out.conditions.em["copper_loss"]
                + state_out.conditions.em["rotor_iron_loss"]
                + state_out.conditions.em["stator_iron_loss"]
                + state_out.conditions.em["magnet_loss"]
            )
        )
        state_out.conditions.windage = {"loss": results, "efficiency": eff}
        print("Efficiency is ", eff)
        return state_out


windage_step = AnalysisStep(
    MyWindageProblemDef, therm.WindageLossAnalyzer, MyWindageLossPostAnalyzer
)

############################ Create Evaluator ########################
evaluator = MachineEvaluator(
    [
        struct_step,
        em_step,
        LengthScaleStep,
        rotor_thermal_step,
        stator_therm_step,
        windage_step,
    ]
)


# evaluate example design if script is run
if __name__ == "__main__":
    from bspm_designer import bspm_designer

    # create machine variant using architect
    free_var = (
        0.00390399,
        0.00964596,
        35.9925,
        0.00358376,
        0.00722451,
        0.0128492,
        0.0143288,
        180.0,
        0.00514122,
        0.00308507,
        0.00363824,
        0.0,
        0.95,
        0,
        0.05,
        20000,
        25,
        80,
    )
    # set operating point for BSPM machine

    design_variant = bspm_designer.create_design(free_var)
    results = evaluator.evaluate(design_variant)
