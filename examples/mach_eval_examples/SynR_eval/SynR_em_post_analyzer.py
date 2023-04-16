import copy
import numpy as np
import os
import sys

from mach_eval.analyzers.torque_data import (
    ProcessTorqueDataProblem,
    ProcessTorqueDataAnalyzer,
)

class SynR_EM_PostAnalyzer:
    def copper_loss(self):
        return 3 * (self.I ** 2) * (self.R_wdg + self.R_wdg_coil_ends + self.R_wdg_coil_sides)

    def get_next_state(results, in_state):
        state_out = copy.deepcopy(in_state)
        machine = state_out.design.machine
        op_pt = state_out.design.settings

        ############################ Extract required info ###########################
        no_of_steps_2nd_TSS = results["no_of_steps_2nd_TSS"]
        no_of_rev_2nd_TSS = results["no_of_rev_2nd_TSS"]
        number_of_total_steps = results["current"].shape[0]
        i1 = number_of_total_steps - no_of_steps_2nd_TSS # index where 2nd time step section begins
        i2 = - int(no_of_steps_2nd_TSS / no_of_rev_2nd_TSS * 0.25) # index where last quarter period of 2nd time step section begins
        omega_m = machine.omega_m
        m = 3
        drive_freq = results["drive_freq"]
        R_wdg = results["stator_wdg_resistances"][0]
        R_wdg_coil_ends = results["stator_wdg_resistances"][1]
        R_wdg_coil_sides = results["stator_wdg_resistances"][2]
        l_st = machine.l_st

        results["current"] = results["current"].iloc[i1:]
        results["voltage"] = results["voltage"].iloc[i1:]
        results["torque"] = results["torque"].iloc[i1:]
        results["iron_loss"] = results["iron_loss"]
        results["hysteresis_loss"] = results["hysteresis_loss"]
        results["eddy_current_loss"] = results["eddy_current_loss"]

        ############################ calculating volumes ###########################

        # shaft volume
        machine = state_out.design.machine
        r_sh = machine.r_ro
        l_st = machine.l_st
        V_sh = np.pi*(r_sh**2)*l_st

        # rotor iron volume
        r_ro    = machine.r_ro
        V_rfe = np.pi*(r_ro**2-r_sh**2)*l_st # <--- needs work

        # # Copper volume
        s_slot = machine.s_slot
        V_scu = machine.Q * machine.Kcu * machine.s_slot

        # # Stator volume
        r_so = machine.r_so
        r_si = machine.r_si
        V_sfe = np.pi * (r_so**2 - r_si**2) * l_st - machine.Q * s_slot * l_st

                ############################ Post-processing #################################
        rotor_mass = (
            V_rfe * 1e-9 * machine.rotor_iron_mat["core_material_density"]
            + V_sh * 1e-9 * machine.shaft_mat["shaft_material_density"]
        )
        rotor_volume = (V_rfe + V_sh) * 1e-9

        ############################ post processing ###########################
        # Torque
        torque_prob = ProcessTorqueDataProblem(results["torque"]["TorCon"])
        torque_analyzer = ProcessTorqueDataAnalyzer()
        torque_avg, torque_ripple = torque_analyzer.analyze(torque_prob)
        TRW = torque_avg / rotor_mass
        TRV = torque_avg / rotor_volume
        PRW = TRW * omega_m
        PRV = TRV * omega_m

        # Losses
        # From JMAG
        stator_iron_loss = results["iron_loss"]["StatorCore"][0]
        rotor_iron_loss = results["iron_loss"]["RotorCore"][0]
        stator_eddy_current_loss = results["eddy_current_loss"]["StatorCore"][0]
        rotor_eddy_current_loss = results["eddy_current_loss"]["RotorCore"][0]
        stator_hysteresis_loss= results["hysteresis_loss"]["StatorCore"][0]
        rotor_hysteresis_loss = results["hysteresis_loss"]["RotorCore"][0]
        stator_ohmic_loss = results["ohmic_loss"]["Coils"].iloc[i2:].mean()
        stator_ohmic_loss_along_stack = stator_ohmic_loss * R_wdg_coil_sides / R_wdg
        stator_ohmic_loss_end_wdg = stator_ohmic_loss * R_wdg_coil_ends / R_wdg
        
        # Calculate stator winding ohmic losses
        I_hat = machine.rated_current * np.sqrt(2)
        stator_calc_ohmic_loss = R_wdg * m / 2 * I_hat ** 2
        stator_calc_ohmic_loss_end_wdg = R_wdg_coil_ends * m / 2 * I_hat ** 2
        stator_calc_ohmic_loss_along_stack = R_wdg_coil_sides * m / 2 * I_hat ** 2

        # Calculating electric loss
        expected_torque = machine.mech_power / omega_m
        scale_ratio = expected_torque / torque_avg
        l_st = l_st * scale_ratio

        rotor_mass = scale_ratio * rotor_mass
        rotor_volume = scale_ratio * rotor_volume

        torque_avg = scale_ratio * torque_avg

        stator_iron_loss = scale_ratio * stator_iron_loss
        rotor_iron_loss = scale_ratio * rotor_iron_loss
        stator_eddy_current_loss = scale_ratio * stator_eddy_current_loss
        rotor_eddy_current_loss = scale_ratio * rotor_eddy_current_loss
        stator_hysteresis_loss = scale_ratio * stator_hysteresis_loss
        rotor_hysteresis_loss = scale_ratio * rotor_hysteresis_loss
        stator_ohmic_loss_along_stack = scale_ratio * stator_ohmic_loss_along_stack
        stator_ohmic_loss = stator_ohmic_loss_along_stack + stator_ohmic_loss_end_wdg
        stator_calc_ohmic_loss_along_stack = scale_ratio * stator_calc_ohmic_loss_along_stack
        stator_calc_ohmic_loss = stator_calc_ohmic_loss_along_stack + stator_calc_ohmic_loss_end_wdg

        # Total losses, output power, and efficiency
        total_losses = (
            stator_iron_loss + rotor_iron_loss + 
            stator_calc_ohmic_loss
        )
        P_out = torque_avg * omega_m
        efficiency = P_out / (P_out + total_losses)

        ############################ Output #################################
        post_processing = {}
        post_processing["torque_avg"] = torque_avg
        post_processing["torque_ripple"] = torque_ripple
        post_processing["TRW"] = TRW
        post_processing["TRV"] = TRV
        post_processing["PRW"] = PRW
        post_processing["PRV"] = PRV
        post_processing["l_st"] = l_st
        post_processing["scale_ratio"] = scale_ratio

        post_processing["rotor_mass"] = rotor_mass
        post_processing["rotor_volume"] = rotor_volume
        # post_processing["motor_mass"] = motor_mass

        post_processing["stator_iron_loss"] = stator_iron_loss
        post_processing["rotor_iron_loss"] = rotor_iron_loss
        post_processing["stator_eddy_current_loss"] = stator_eddy_current_loss
        post_processing["rotor_eddy_current_loss"] = rotor_eddy_current_loss
        post_processing["stator_hysteresis_loss"] = stator_hysteresis_loss
        post_processing["rotor_hysteresis_loss"] = rotor_hysteresis_loss
        post_processing["stator_ohmic_loss"] = stator_ohmic_loss
        post_processing["stator_ohmic_loss_along_stack"] = stator_ohmic_loss_along_stack
        post_processing["stator_ohmic_loss_end_wdg"] = stator_ohmic_loss_end_wdg
        post_processing["stator_calc_ohmic_loss"] = stator_calc_ohmic_loss
        post_processing["stator_calc_ohmic_loss_along_stack"] = stator_calc_ohmic_loss_along_stack
        post_processing["stator_calc_ohmic_loss_end_wdg"] = stator_calc_ohmic_loss_end_wdg
        post_processing["total_losses"] = total_losses
        post_processing["output_power"] = P_out
        post_processing["efficiency"] = efficiency

        state_out.conditions.em = post_processing

        print("\n************************ EM RESULT ************************")
        print("Scaling factor = ", scale_ratio)
        print("Torque = ", torque_avg, " Nm")
        print("Torque density = ", TRV, " Nm/m3",)
        print("Torque ripple = ", torque_ripple)
        print("Power = ", P_out, " W")
        print("Power density = ", PRV, " W/m3",)
        print("Efficiency = ", efficiency * 100, " %")
        print("************************************************************\n")

        return state_out