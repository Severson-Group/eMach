import os
import sys
from copy import deepcopy
import numpy as np

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory 3 levels above this file's directory to path for module import
sys.path.append("../../..")

from mach_eval.analyzers.electromagnetic.bspm import jmag_2d_analyzer as em
from mach_eval.analyzers.electromagnetic.bspm.jmag_2d_config import JMAG_2D_Config
from mach_eval.analyzers.mechanical import rotor_structural as stra
from mach_eval.analyzers.mechanical import rotor_thermal as therm
from mach_eval.analyzers.mechanical import thermal_stator as st_therm
from mach_eval.analyzers.mechanical import windage_loss as wl
from bpsm_em_post_analyzer import BSPM_EM_PostAnalyzer
from length_scale_step import LengthScaleStep
from mach_eval import AnalysisStep, MachineEvaluator, ProblemDefinition
from mach_opt import InvalidDesign

# reset to current file path for JMAG_FEA_Configuration
# os.chdir(os.path.dirname(__file__))


############################ Define Struct AnalysisStep ######################
stress_limits = {
    "rad_sleeve": -100e6,
    "tan_sleeve": 1300e6,
    "rad_magnets": 0,
    "tan_magnets": 80e6,
}
# spd = sta.SleeveProblemDef(design_variant)
# problem = spd.get_problem()
struct_ana = stra.SPM_RotorSleeveAnalyzer(stress_limits)


class MySleeveProblemDef(ProblemDefinition):
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

        r_sh = design.machine.r_sh
        r_ro = design.machine.r_ro
        d_m = design.machine.d_m
        N = design.settings.speed
        deltaT = design.settings.rotor_temp_rise

        problem = stra.SPM_RotorSleeveProblem(r_sh, d_m, r_ro, deltaT, material_dict, N)
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
class BSPM_EM_ProblemDefinition(ProblemDefinition):
    """Converts a State into a problem"""

    def __init__(self):
        pass

    def get_problem(state):
        problem = em.BSPM_EM_Problem(state.design.machine, state.design.settings)
        return problem


# initialize em analyzer class with FEA configuration
jmag_config = JMAG_2D_Config(
    no_of_rev_1TS=3,
    no_of_rev_2TS=0.5,
    no_of_steps_per_rev_1TS=8,
    no_of_steps_per_rev_2TS=64,
    mesh_size=4e-3,
    magnet_mesh_size=2e-3,
    airgap_mesh_radial_div=5,
    airgap_mesh_circum_div=720,
    mesh_air_region_scale=1.15,
    only_table_results=False,
    csv_results=(r"Torque;Force;FEMCoilFlux;LineCurrent;TerminalVoltage;JouleLoss;TotalDisplacementAngle;"
                  "JouleLoss_IronLoss;IronLoss_IronLoss;HysteresisLoss_IronLoss"),
    del_results_after_calc=False,
    run_folder=os.path.abspath("") + "/run_data/",
    jmag_csv_folder=os.path.abspath("") + "/run_data/JMAG_csv/",
    max_nonlinear_iterations=50,
    multiple_cpus=True,
    jmag_scheduler=False,
    jmag_visible=False,
)
em_analysis = em.BSPM_EM_Analyzer(jmag_config)
# define AnalysysStep for EM evaluation
em_step = AnalysisStep(BSPM_EM_ProblemDefinition, em_analysis, BSPM_EM_PostAnalyzer)

###################### Define Rotor Thermal AnalysisStep #####################
class MyAirflowProblemDef(ProblemDefinition):
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
            r_sh=r_sh,
            d_ri=d_ri,
            r_ro=r_ro,
            d_sl=d_sl,
            r_si=r_si,
            l_st=l_st,
            l_hub=l_hub,
            T_ref=T_ref,
            losses=losses,
            omega=omega,
            max_temp=rotor_max_temp,
            mat_dict=material_dict,
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
        print("Magnet temperature is ", results["magnet Temp"])
        print("Required airflow is ", results["Required Airflow"])
        return state_out


rotor_thermal_step = AnalysisStep(
    MyAirflowProblemDef, therm.AirflowAnalyzer(), MyAirflowPostAnalyzer
)

###################### Define Stator Thermal AnalysisStep #####################
class MyThermalProblemDefinition(ProblemDefinition):
    """Class converts input state into a problem"""

    def get_problem(state):
        """Returns Problem from Input State"""
        # TODO define problem definition
        g_sy = state.conditions.g_sy  # Volumetric loss in Stator Yoke [W/m^3]
        g_th = state.conditions.g_th  # Volumetric loss in Stator Tooth [W/m^3]
        w_st = state.design.machine.w_st  # Tooth width [m]
        l_st = state.design.machine.l_st  # Stack length [m]
        r_sy = state.design.machine.r_so - state.design.machine.d_sy
        alpha_q = 2 * np.pi / state.design.machine.Q  # [rad]
        r_so = state.design.machine.r_so  # outer stator radius [m]

        k_ins = 1  # thermal insulation conductivity (~1)
        w_ins = 0.5e-3  # insulation thickness [m] (.5mm)
        k_fe = state.design.machine.stator_iron_mat["core_therm_conductivity"]
        h = 100  # convection co-eff W/m^2K
        alpha_slot = alpha_q - 2 * np.arctan(
            w_st / (2 * r_sy)
        )  # span of back of stator slot [rad]
        T_ref = 20  # temperature of cooling liquid [K]

        r_si = state.design.machine.r_si  # inner stator radius
        Q_coil = state.conditions.Q_coil  # ohmic loss per coil
        h_slot = 0  # in slot convection coeff [W/m^2K] set to 0

        problem = st_therm.StatorThermalProblem(
            g_sy=g_sy,
            g_th=g_th,
            w_tooth=w_st,
            l_st=l_st,
            alpha_q=alpha_q,
            r_si=r_si,
            r_so=r_so,
            r_sy=r_sy,
            k_ins=k_ins,
            w_ins=w_ins,
            k_fe=k_fe,
            h=h,
            alpha_slot=alpha_slot,
            Q_coil=Q_coil,
            h_slot=h_slot,
            T_ref=T_ref,
        )
        return problem


class MyStatorThermalPostAnalyzer:
    """Converts input state into output state for TemplateAnalyzer"""

    def get_next_state(results, stateIn):
        if results["Coil temperature"] > 300 == True:
            raise InvalidDesign("Magnet temperature beyond limits")
        else:
            stateOut = deepcopy(stateIn)
            stateOut.conditions.T_coil = results["Coil temperature"]
            stateOut.conditions.T_sy = results["Stator yoke temperature"]

        print("Coil Temp is ", results["Coil temperature"])
        print("Stator Temp is ", results["Stator yoke temperature"])
        return stateOut


stator_therm_step = AnalysisStep(
    MyThermalProblemDefinition,
    st_therm.StatorThermalAnalyzer(),
    MyStatorThermalPostAnalyzer,
)

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
        print("Efficiency is ", eff)
        return state_out


windage_step = AnalysisStep(
    MyWindageProblemDef, wl.WindageLossAnalyzer, MyWindageLossPostAnalyzer
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
    from bspm_designer import designer

    # create machine variant using architect
    free_var = (
        0.00275,
        0.01141,
        44.5,
        0.00542,
        0.00909,
        0.0169,
        0.0135,
        178.78,
        0.00371,
        0.00307,
        0.00489,
        0.0,
        0.975,
        0,
        0.025,
        160000,
        25,
        55,
    )
    # set operating point for BSPM machine

    design_variant = designer.create_design(free_var)
    results = evaluator.evaluate(design_variant)
