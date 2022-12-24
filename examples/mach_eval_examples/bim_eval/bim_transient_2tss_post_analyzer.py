import copy
import numpy as np
import os
import sys

# Add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")
print(os.path.dirname(__file__)+"/../../..")

from mach_eval.analyzers.force_vector_data import (
    ProcessForceDataProblem,
    ProcessForceDataAnalyzer,
)
from mach_eval.analyzers.torque_data import (
    ProcessTorqueDataProblem,
    ProcessTorqueDataAnalyzer,
)
from mach_eval.analyzers.mechanical.windage_loss import (
    WindageLossProblem,
    WindageLossAnalyzer,
)


class BIM_Transient_2TSS_PostAnalyzer:
    def get_next_state(results, in_state):
        state_out = copy.deepcopy(in_state)
        machine = state_out.design.machine
        op_pt = state_out.design.settings

        ############################ Extract required info ###########################
        config = results["analyzer_configurations"]
        no_of_steps_2nd_TSS = config.no_of_steps_2nd_TSS
        no_of_rev_2nd_TSS = config.no_of_rev_2nd_TSS
        number_of_total_steps = results["current"].shape[0]
        i1 = number_of_total_steps - no_of_steps_2nd_TSS # index where 2nd time step section begins
        i2 = - int(no_of_steps_2nd_TSS / no_of_rev_2nd_TSS * 0.25) # index where last quarter period of 2nd time step section begins
        slip_freq = results["slip_freq"]
        drive_freq = results["drive_freq"]
        omega_m = machine.omega_m
        m = machine.no_of_phases
        R_wdg = results["stator_wdg_resistances"][0]
        R_wdg_coil_ends = results["stator_wdg_resistances"][1]
        R_wdg_coil_sides = results["stator_wdg_resistances"][2]
        l_st = machine.l_st

        results["current"] = results["current"].iloc[i1:]
        results["torque"] = results["torque"].iloc[i1:]
        results["force"] = results["force"].iloc[i1:]
        results["voltage"] = results["voltage"].iloc[i1:]
        results["hysteresis_loss"] = results["hysteresis_loss"]
        results["iron_loss"] = results["iron_loss"]
        results["eddy_current_loss"] = results["eddy_current_loss"]
        results["ohmic_loss"] = results["ohmic_loss"].iloc[i1:]

        ############################ Post-processing #################################
        rotor_mass = (
            machine.V_rfe * 1e-9 * machine.rotor_iron_mat["core_material_density"]
            + machine.V_shaft * 1e-9 * machine.shaft_mat["shaft_material_density"]
            + results["V_r_cage"] * 1e-9 * machine.rotor_bar_mat["bar_material_density"]
        )
        rotor_volume = machine.V_rotor * 1e-9
            # motor mass:
            # weight = machine.V_rfe * rotor_iron['core_material_density'] + \
            #          machine.V_sh * shaft['shaft_material_density'] + \
            #          machine.V_rPM * magnet['magnet_material_density'] + \
            #          machine.V_sfe * stator_iron['core_material_density'] + \
            #          machine.V_scu * coil['copper_material_density']

        
        # Torque
        torque_prob = ProcessTorqueDataProblem(results["torque"]["TorCon"])
        torque_avg, torque_ripple = ProcessTorqueDataAnalyzer.analyze(torque_prob)
        TRW = torque_avg / rotor_mass
        TRV = torque_avg / rotor_volume

        # Force
        if r"ForCon:X Component" in results["force"]: # older jmag versions
            Fx = results["force"][r"ForCon:X Component"]
            Fy = results["force"][r"ForCon:Y Component"]
        elif r"ForCon:1st" in results["force"]: # jmag version 21
            Fx = results["force"][r"ForCon:1st"]
            Fy = results["force"][r"ForCon:2nd"]

        force_problem = ProcessForceDataProblem(Fx=Fx, Fy=Fy)
        force_analyzer = ProcessForceDataAnalyzer()
        Fx_avg, Fy_avg, F_abs_avg, Em, Ea = force_analyzer.analyze(force_problem)
        FRW = F_abs_avg / (9.81 * rotor_mass)
        FRV = F_abs_avg / rotor_volume

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
        rotor_ohmic_loss_along_stack = results["ohmic_loss"]["Cage"].iloc[i2:].mean()
        
        # Calculate stator winding ohmic losses
        It_hat = op_pt.It_ratio * machine.rated_current * np.sqrt(2)
        Is_hat = op_pt.Is_ratio * machine.rated_current * np.sqrt(2)
        stator_calc_ohmic_loss = R_wdg * m / 2 * (It_hat ** 2 + Is_hat**2)
        stator_calc_ohmic_loss_end_wdg = R_wdg_coil_ends * m / 2 * (It_hat ** 2 + Is_hat**2)
        stator_calc_ohmic_loss_along_stack = R_wdg_coil_sides * m / 2 * (It_hat ** 2 + Is_hat**2)

        # Calculate rotor cage ohmic losses (using last 1/4th of a cycle)
        currents = results["current"].iloc[i2:]
        R_bar = results["rotor_cage_resistances"][0]
        R_end_ring = results["rotor_cage_resistances"][1]
        P1, P2, P3 = calculate_rotor_cage_ohmic_losses(
            machine, currents, results["conductor_names"], 
            config.non_zero_end_ring_res, R_end_ring, R_bar)
        rotor_calc_ohmic_loss = P1
        rotor_calc_ohmic_loss_along_stack = P2
        rotor_calc_ohmic_loss_end_rings = P3

        # Scaling
        if config.scale_axial_length == True:
            expected_torque = machine.mech_power / omega_m
            scale_ratio = expected_torque / torque_avg
            l_st = l_st * scale_ratio

            rotor_mass = scale_ratio * rotor_mass
            rotor_volume = scale_ratio * rotor_volume

            torque_avg = scale_ratio * torque_avg
            results["breakdown_torque_from_tha"] = scale_ratio * results["breakdown_torque_from_tha"]
            Fx_avg = scale_ratio * Fx_avg
            Fy_avg = scale_ratio * Fy_avg
            F_abs_avg = scale_ratio * F_abs_avg

            stator_iron_loss = scale_ratio * stator_iron_loss
            rotor_iron_loss = scale_ratio * rotor_iron_loss
            stator_eddy_current_loss = scale_ratio * stator_eddy_current_loss
            rotor_eddy_current_loss = scale_ratio * rotor_eddy_current_loss
            stator_hysteresis_loss = scale_ratio * stator_hysteresis_loss
            rotor_hysteresis_loss = scale_ratio * rotor_hysteresis_loss
            stator_ohmic_loss_along_stack = scale_ratio * stator_ohmic_loss_along_stack
            stator_ohmic_loss = stator_ohmic_loss_along_stack + stator_ohmic_loss_end_wdg
            rotor_ohmic_loss_along_stack = scale_ratio * rotor_ohmic_loss_along_stack
            stator_calc_ohmic_loss_along_stack = scale_ratio * stator_calc_ohmic_loss_along_stack
            stator_calc_ohmic_loss = stator_calc_ohmic_loss_along_stack + stator_calc_ohmic_loss_end_wdg
            rotor_calc_ohmic_loss_along_stack = scale_ratio * rotor_calc_ohmic_loss_along_stack
            rotor_calc_ohmic_loss = rotor_calc_ohmic_loss_along_stack + rotor_calc_ohmic_loss_end_rings

        # Calculate windage loss
        windage_loss_prob = WindageLossProblem(
            Omega=omega_m, R_ro=machine.r_ro/1000, stack_length=l_st/1000,
            R_st=machine.r_si/1000, u_z=0, T_air=op_pt.ambient_temp
            )
        [windage_loss_radial, windage_loss_endFace, windage_loss_axial] = WindageLossAnalyzer.analyze(windage_loss_prob)
        windage_loss = windage_loss_radial + windage_loss_endFace + windage_loss_axial
        windage_loss_2 = get_windage_loss(machine, l_st, omega_m, TEMPERATURE_OF_AIR=op_pt.ambient_temp)

        # Total losses, output power, and efficiency
        total_losses = (
            stator_iron_loss + rotor_iron_loss + 
            stator_calc_ohmic_loss + rotor_calc_ohmic_loss + 
            windage_loss
        )
        P_out = torque_avg * omega_m
        efficiency = P_out / (P_out + total_losses)


        ############################ Output #################################
        post_processing = {}
        post_processing["torque_avg"] = torque_avg
        post_processing["torque_ripple"] = torque_ripple
        post_processing["TRW"] = TRW
        post_processing["TRV"] = TRV
        post_processing["breakdown_slip_freq_tha"] = slip_freq
        post_processing["breakdown_torque_from_tha"] = results["breakdown_torque_from_tha"]
        post_processing["l_st"] = l_st
        post_processing["scale_ratio"] = scale_ratio

        post_processing["Fx_avg"] = Fx_avg
        post_processing["Fy_avg"] = Fy_avg
        post_processing["Favg"] = F_abs_avg
        post_processing["FRW"] = FRW
        post_processing["FRV"] = FRV
        post_processing["rotor_mass"] = rotor_mass
        post_processing["rotor_volume"] = rotor_volume
        # post_processing["motor_mass"] = motor_mass
        post_processing["Em"] = Em
        post_processing["Ea"] = Ea

        post_processing["stator_iron_loss"] = stator_iron_loss
        post_processing["rotor_iron_loss"] = rotor_iron_loss
        post_processing["stator_eddy_current_loss"] = stator_eddy_current_loss
        post_processing["rotor_eddy_current_loss"] = rotor_eddy_current_loss
        post_processing["stator_hysteresis_loss"] = stator_hysteresis_loss
        post_processing["rotor_hysteresis_loss"] = rotor_hysteresis_loss
        post_processing["stator_ohmic_loss"] = stator_ohmic_loss
        post_processing["stator_ohmic_loss_along_stack"] = stator_ohmic_loss_along_stack
        post_processing["stator_ohmic_loss_end_wdg"] = stator_ohmic_loss_end_wdg
        post_processing["rotor_ohmic_loss_along_stack"] = rotor_ohmic_loss_along_stack
        post_processing["stator_calc_ohmic_loss"] = stator_calc_ohmic_loss
        post_processing["stator_calc_ohmic_loss_along_stack"] = stator_calc_ohmic_loss_along_stack
        post_processing["stator_calc_ohmic_loss_end_wdg"] = stator_calc_ohmic_loss_end_wdg
        post_processing["rotor_calc_ohmic_loss"] = rotor_calc_ohmic_loss
        post_processing["rotor_calc_ohmic_loss_along_stack"] = rotor_calc_ohmic_loss_along_stack
        post_processing["rotor_calc_ohmic_loss_end_rings"] = rotor_calc_ohmic_loss_end_rings
        post_processing["windage_loss"] = windage_loss
        post_processing["total_losses"] = total_losses
        post_processing["output_power"] = P_out
        post_processing["efficiency"] = efficiency

        state_out.conditions.em = post_processing

        print("\n************************ EM RESULT ************************")
        print("Scaling factor = ", scale_ratio)
        print("Torque = ", torque_avg, " Nm")
        print("Torque density = ", TRV, " Nm/m3",)
        print("Power = ", P_out, " W")
        print("Efficiency = ", efficiency * 100, " %")

        print("Force = ", F_abs_avg, " N")
        print("Force per rotor weight = ", FRW, " pu")
        print("Force error angle = ", Ea, " deg")
        print("************************************************************\n")

        return state_out


def calculate_rotor_cage_ohmic_losses(machine, currents, conductor_names, non_zero_end_ring_res, R_end_ring, R_bar):
    ohmic_losses_bars = []
    ohmic_losses_end_ring1 = []
    ohmic_losses_end_ring2 = []

    phases = machine.name_phases_rotor

    for i in range(len(conductor_names)):
        ohmic_losses_bars.append(
            (R_bar * currents[conductor_names[i]] ** 2).mean()
        )

    if non_zero_end_ring_res == True:
        for i in range(len(phases)):
            end_ring_1 = "R_" + phases[i] + "_1"
            end_ring_2 = "R_" + phases[i] + "_2"

            ohmic_losses_end_ring1.append(
                (R_end_ring * currents[end_ring_1] ** 2).mean()
            )
            ohmic_losses_end_ring2.append(
                (R_end_ring * currents[end_ring_2] ** 2).mean()
            )
    else:
        for i in range(len(phases)):
            ohmic_losses_end_ring1.append(0)
            ohmic_losses_end_ring2.append(0)

    rotor_calc_ohmic_loss_along_stack = sum(ohmic_losses_bars)
    rotor_calc_ohmic_loss_end_rings = sum(ohmic_losses_end_ring1) + sum(ohmic_losses_end_ring2)
    rotor_calc_ohmic_loss = rotor_calc_ohmic_loss_along_stack + rotor_calc_ohmic_loss_end_rings

    return rotor_calc_ohmic_loss, rotor_calc_ohmic_loss_along_stack, rotor_calc_ohmic_loss_end_rings


# From Jiahao's code
def get_windage_loss(machine, l_st, Omega, TEMPERATURE_OF_AIR=25):

    # %Air friction loss calculation
    nu_0_Air  = 13.3e-6#;  %[m^2/s] kinematic viscosity of air at 0
    rho_0_Air = 1.29#;     %[kg/m^3] Air density at 0
    Shaft = [l_st,                               #1;         %End position of the sections mm (Absolut)
             machine.r_ro + machine.delta_e, #1;         %Inner Radius in mm
             1,                                                     #0;         %Shrouded (1) or free surface (0)
             machine.delta_e]                              #0];        %Airgap in mm
    Num_shaft_section = 1
    T_Air = TEMPERATURE_OF_AIR #20:(120-20)/((SpeedMax-SpeedMin)/SpeedStep):120         #; % Air temperature []
    
    nu_Air  = nu_0_Air*((T_Air+273)/(0+273))**1.76
    rho_Air = rho_0_Air*(0+273)/(T_Air+273)
    windage_loss_radial = 0 

    # Calculation of the section number_of_total_steps ...
    L     = Shaft[0]*1e-3 # in meter
    R     = Shaft[1]*1e-3 # radius of air gap
    delta = Shaft[3]*1e-3 # number_of_total_steps of air gap

    # Reynolds number
    Rey = R**2 * (Omega)/nu_Air

    if Rey <= 170:
        c_W = 8. / Rey
    elif Rey>170 and Rey<4000:
        c_W = 0.616*Rey**(-0.5)
    else:
        c_W = 6.3e-2*Rey**(-0.225)
    windage_loss_radial = c_W*np.pi*rho_Air* Omega**3 * R**5 * (1.+L/R)

    # # shrouded cylinder by air gap from <Loss measurement of a 30 kW High Speed Permanent Magnet Synchronous Machine with Active Magnetic Bearings>
    # Tay = R*(Omega)*(delta/nu_Air)*np.sqrt(delta/R) # Taylor number 
    # if Rey <= 170:
    #     c_W = 8. / Rey
    # elif Rey>170 and Tay<41.3:
    #     # c_W = 1.8 * Rey**(-1) * delta/R**(-0.25) * (R+delta)**2 / ((R+delta)**2 - R**2) # Ye gu's codes
    #     c_W = 1.8 * (R/delta)**(0.25) * (R+delta)**2 / (Rey*delta**2) # Ashad over Slack 2019/11/21
    # else:
    #     c_W = 7e-3
    # windage_loss_radial = c_W*np.pi*rho_Air* Omega**3 * R**4 * L
        
    # end friction loss added - 05192018.yegu
    # the friction coefficients from <Rotor Design of a High-Speed Permanent Magnet Synchronous Machine rating 100,000 rpm at 10 kW>
    Rer = rho_Air * (machine.r_ro * 1e-3)**2 * Omega/nu_Air
    if Rer <= 30:
        c_f = 64/3. / Rer
    elif Rer>30 and Rer<3*10**5:
        c_f = 3.87 * Rer**(-0.5)
    else:
        c_f = 0.146 * Rer**(-0.2)

    windage_loss_axial = 0.5 * c_f * rho_Air * Omega**3 * (machine.r_ro*1e-3)**5
    
    windage_loss_total = windage_loss_radial + windage_loss_axial
    return windage_loss_total