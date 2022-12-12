import copy
import numpy as np
import os
import sys

# add the directory 3 levels above this file's directory to path for module import
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


class BIM_Transient_2TSS_PostAnalyzer:
    def get_next_state(results, in_state):
        state_out = copy.deepcopy(in_state)
        machine = state_out.design.machine
        op_pt = state_out.design.settings

        ############################ extract required info ###########################
        length = results["current"].shape[0]
        i = length - results["range_fine_step"]
        i1 = - int(0.5 * results["range_fine_step"]) # used to calculate average ohmic losses
        results["current"] = results["current"].iloc[i:]

        results["torque"] = results["torque"].iloc[i:]
        results["force"] = results["force"].iloc[i:]
        results["voltage"] = results["voltage"].iloc[i:]
        results["hysteresis_loss"] = results["hysteresis_loss"]
        results["iron_loss"] = results["iron_loss"]
        results["eddy_current_loss"] = results["eddy_current_loss"]
        results["ohmic_loss"] = results["ohmic_loss"].iloc[i:]

        ############################ post processing #################################
        rotor_mass = (
            machine.V_rfe * 1e-9 * machine.rotor_iron_mat["core_material_density"]
            + machine.V_shaft * 1e-9 * machine.shaft_mat["shaft_material_density"]
            + machine.V_r_cage * 1e-9 * machine.rotor_bar_mat["bar_material_density"]
        )
        
        # Average torque, torque ripple
        torque_prob = ProcessTorqueDataProblem(results["torque"]["TorCon"])
        torque_avg, torque_ripple = ProcessTorqueDataAnalyzer.analyze(torque_prob)

        # Average force, average Fx and Fy
        force_prob = ProcessForceDataProblem(
            Fx=results["force"][r"ForCon:X Component"],
            Fy=results["force"][r"ForCon:Y Component"],
        )
        force_ana = ProcessForceDataAnalyzer()
        Fx, Fy, force_avg, Em, Ea = force_ana.analyze(force_prob)

        # Losses
        # Calculate rotor cage ohmic losses (using last 1/4th of a cycle)
        currents = results["current"].iloc[i1:]
        P1, P2, P3 = calculate_rotor_cage_ohmic_losses(machine, currents, results["conductor_names"], results["non_zero_end_ring_res"])
        rotor_calc_ohmic_loss = P1
        rotor_calc_ohmic_loss_along_stack = P2
        rotor_calc_ohmic_loss_end_rings = P3

        windage_loss = get_windage_loss(machine, op_pt)



        post_processing = {}
        post_processing["torque_avg"] = torque_avg
        post_processing["torque_ripple"] = torque_ripple
        # post_processing["slip_freq"] = state_out.conditions.time_harmonic_results["slip_freq_breakdown_torque"]

        post_processing["Fx"] = Fx
        post_processing["Fy"] = Fy
        post_processing["Favg"] = force_avg

        post_processing["TRW"] = torque_avg / rotor_mass
        post_processing["TRV"] = torque_avg / (machine.V_rotor * 1e-9)
        post_processing["FRW"] = force_avg / rotor_mass
        post_processing["rotor_mass"] = rotor_mass
        post_processing["Em"] = Em
        post_processing["Ea"] = Ea

        post_processing["stator_iron_loss"] = results["iron_loss"]["StatorCore"][0]
        post_processing["rotor_iron_loss"] = results["iron_loss"]["RotorCore"][0]
        post_processing["stator_eddy_current_loss"] = results["eddy_current_loss"]["StatorCore"][0]
        post_processing["rotor_eddy_current_loss"] = results["eddy_current_loss"]["RotorCore"][0]
        post_processing["stator_hysteresis_loss"] = results["hysteresis_loss"]["StatorCore"][0]
        post_processing["rotor_hysteresis_loss"] = results["hysteresis_loss"]["RotorCore"][0]
        post_processing["stator_ohmic_loss_along_stack"] = results["ohmic_loss"]["Coils"].iloc[i1:].mean()
        post_processing["rotor_ohmic_loss_along_stack"] = results["ohmic_loss"]["Cage"].iloc[i1:].mean()
        
        post_processing["stator_calc_ohmic_loss"] = results["stator_calc_ohmic_loss"][0]
        post_processing["stator_calc_ohmic_loss_along_stack"] = results["stator_calc_ohmic_loss"][1]
        post_processing["stator_calc_ohmic_loss_end_wdg"] = results["stator_calc_ohmic_loss"][2]
        post_processing["rotor_calc_ohmic_loss"] = rotor_calc_ohmic_loss
        post_processing["rotor_calc_ohmic_loss_along_stack"] = rotor_calc_ohmic_loss_along_stack
        post_processing["rotor_calc_ohmic_loss_end_rings"] = rotor_calc_ohmic_loss_end_rings
        post_processing["windage_loss"] = windage_loss


        total_losses = (
            post_processing["stator_iron_loss"] + post_processing["rotor_iron_loss"] + 
            post_processing["stator_calc_ohmic_loss"] + post_processing["rotor_calc_ohmic_loss"] + 
            post_processing["windage_loss"]
        )

        P_out = torque_avg * (op_pt.drive_freq - op_pt.slip_freq) / machine.p * 2 * np.pi
        efficiency = P_out / (P_out + total_losses)

        post_processing["total_losses"] = total_losses
        post_processing["output_power"] = P_out
        post_processing["efficiency"] = efficiency

        # post_processing["phase_voltage_rms"] = compute_vrms(results["voltage"])
        # post_processing["power_factor"] = compute_power_factor(
        #     results["voltage"],
        #     results["current"],
        #     target_freq=machine.mech_omega * machine.p / (2 * np.pi),
        # )

        state_out.conditions.em = post_processing

        print("\n************************ EM RESULT ************************")
        print("Torque = ", torque_avg, " Nm")
        print("Torque density = ", torque_avg / (machine.V_rotor * 1e-9), " Nm/m3",)
        print("Power = ", P_out, " W")
        print("Efficiency = ", efficiency, " %")

        FRW = force_avg / (rotor_mass * 9.8)

        print("Force = ", force_avg, " N")
        print("Force per rotor weight = ", FRW, " pu")
        print("Force error angle = ", Ea, " deg")
        print("************************************************************\n")

        return state_out

# machine, currents, results["conductor_names"]
def calculate_rotor_cage_ohmic_losses(machine, currents, conductor_names, non_zero_end_ring_res):
    ohmic_losses_bars = []
    ohmic_losses_end_ring1 = []
    ohmic_losses_end_ring2 = []
    R_end_ring = machine.R_end_ring
    R_rotor_bar = machine.R_rotor_bar

    phases = machine.name_phases_rotor

    for i in range(len(conductor_names)):
        ohmic_losses_bars.append(
            (R_rotor_bar * currents[conductor_names[i]] ** 2).mean()
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
def get_windage_loss(machine, op_pt, TEMPERATURE_OF_AIR=75):

    # %Air friction loss calculation
    nu_0_Air  = 13.3e-6#;  %[m^2/s] kinematic viscosity of air at 0
    rho_0_Air = 1.29#;     %[kg/m^3] Air density at 0
    Shaft = [machine.l_st,                               #1;         %End position of the sections mm (Absolut)
             machine.r_ro + machine.delta_e, #1;         %Inner Radius in mm
             1,                                                     #0;         %Shrouded (1) or free surface (0)
             machine.delta_e]                              #0];        %Airgap in mm
    Num_shaft_section = 1
    T_Air = TEMPERATURE_OF_AIR #20:(120-20)/((SpeedMax-SpeedMin)/SpeedStep):120         #; % Air temperature []
    
    nu_Air  = nu_0_Air*((T_Air+273)/(0+273))**1.76
    rho_Air = rho_0_Air*(0+273)/(T_Air+273)
    windage_loss_radial = 0 

    # Calculation of the section length ...
    L     = Shaft[0]*1e-3 # in meter
    R     = Shaft[1]*1e-3 # radius of air gap
    delta = Shaft[3]*1e-3 # length of air gap
    
    Omega = (op_pt.drive_freq - op_pt.slip_freq) / machine.p * 2 * np.pi

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



def compute_vrms(voltage_df):
    phase_voltage = voltage_df["Terminal_Wt"]
    rms_voltage = np.sqrt(sum(np.square(phase_voltage)) / len(phase_voltage))
    return rms_voltage


def compute_power_factor(
    voltage_df, current_df, target_freq, numPeriodicalExtension=1000
):
    mytime = current_df.index
    voltage = voltage_df["Terminal_Wt"]
    current = current_df["coil_Wb"]

    power_factor = compute_power_factor_from_half_period(
        voltage,
        current,
        mytime,
        targetFreq=target_freq,
        numPeriodicalExtension=numPeriodicalExtension,
    )
    return power_factor


# https://dsp.stackexchange.com/questions/11513/estimate-frequency-and-peak-value-of-a-signals-fundamental
# define N_SAMPLE ((long int)(1.0/(0.1*TS))) // Resolution 0.1 Hz = 1 / (N_SAMPLE * TS)
class GoertzelDataStruct(object):
    """docstring for GoertzelDataStruct"""

    def __init__(
        self,
        id=None,
    ):
        self.id = id
        self.bool_initialized = False
        self.sine = None
        self.cosine = None
        self.coeff = None
        self.scalingFactor = None
        self.q = None
        self.q2 = None
        self.count = None
        self.k = None  # k is the normalized target frequency
        self.real = None
        self.imag = None
        self.accumSquaredData = None
        self.ampl = None
        self.phase = None

    # /************************************************
    #  * Real time implementation to avoid the array of input double *data[]
    #  * with Goertzel Struct to store the variables and the output values
    #  *************************************************/
    def goertzel_realtime(gs, targetFreq, numSamples, samplingRate, data):
        # gs is equivalent to self
        try:
            len(data)
        except:
            pass
        else:
            raise Exception(
                "This is for real time implementation of Goertzel, hence data must be a scalar rather than array."
            )

        if not gs.bool_initialized:
            gs.bool_initialized = True

            gs.count = 0
            gs.k = 0.5 + ((numSamples * targetFreq) / samplingRate)
            omega = (2.0 * np.pi * gs.k) / numSamples
            gs.sine = np.sin(omega)
            gs.cosine = np.cos(omega)
            gs.coeff = 2.0 * gs.cosine
            gs.q1 = 0
            gs.q2 = 0
            gs.scalingFactor = 0.5 * numSamples
            gs.accumSquaredData = 0.0

        q0 = gs.coeff * gs.q1 - gs.q2 + data
        gs.q2 = gs.q1
        gs.q1 = (
            q0  # // q1 is the newest output vk[N], while q2 is the last output vk[N-1].
        )

        gs.accumSquaredData += data * data

        gs.count += 1
        if gs.count >= numSamples:
            # // calculate the real and imaginary results with scaling appropriately
            gs.real = (
                gs.q1 * gs.cosine - gs.q2
            ) / gs.scalingFactor  # // inspired by the python script of sebpiq
            gs.imag = (gs.q1 * gs.sine) / gs.scalingFactor

            # // reset
            gs.bool_initialized = False
            return True
        else:
            return False

    def goertzel_offline(gs, targetFreq, samplingRate, data_list):
        # gs is equivalent to self
        numSamples = len(data_list)
        if not gs.bool_initialized:
            gs.bool_initialized = True

            gs.count = 0
            gs.k = 0.5 + ((numSamples * targetFreq) / samplingRate)
            omega = (2.0 * np.pi * gs.k) / numSamples
            gs.sine = np.sin(omega)
            gs.cosine = np.cos(omega)
            gs.coeff = 2.0 * gs.cosine
            gs.q1 = 0
            gs.q2 = 0
            gs.scalingFactor = 0.5 * numSamples
            gs.accumSquaredData = 0.0

        for data in data_list:
            q0 = gs.coeff * gs.q1 - gs.q2 + data
            gs.q2 = gs.q1
            gs.q1 = q0  # // q1 is the newest output vk[N], while q2 is the last output vk[N-1].

            gs.accumSquaredData += data * data

            gs.count += 1
            if gs.count >= numSamples:
                # // calculate the real and imaginary results with scaling appropriately
                gs.real = (
                    gs.q1 * gs.cosine - gs.q2
                ) / gs.scalingFactor  # // inspired by the python script of sebpiq
                gs.imag = (gs.q1 * gs.sine) / gs.scalingFactor

                # // reset
                gs.bool_initialized = False
                return True
        return None


def compute_power_factor_from_half_period(
    voltage, current, mytime, targetFreq=1e3, numPeriodicalExtension=1000
):
    gs_u = GoertzelDataStruct("Goertzel Struct for Voltage\n")
    gs_i = GoertzelDataStruct("Goertzel Struct for Current\n")

    TS = mytime[-1] - mytime[-2]

    if type(voltage) != type([]):
        voltage = voltage.tolist() + (-voltage).tolist()
        current = current.tolist() + (-current).tolist()
    else:
        voltage = voltage + [-el for el in voltage]
        current = current + [-el for el in current]

    voltage *= numPeriodicalExtension
    current *= numPeriodicalExtension

    gs_u.goertzel_offline(targetFreq, 1.0 / TS, voltage)
    gs_i.goertzel_offline(targetFreq, 1.0 / TS, current)

    gs_u.ampl = np.sqrt(gs_u.real * gs_u.real + gs_u.imag * gs_u.imag)
    gs_u.phase = np.arctan2(gs_u.imag, gs_u.real)

    gs_i.ampl = np.sqrt(gs_i.real * gs_i.real + gs_i.imag * gs_i.imag)
    gs_i.phase = np.arctan2(gs_i.imag, gs_i.real)

    phase_difference_in_deg = (gs_i.phase - gs_u.phase) / np.pi * 180
    power_factor = np.cos(gs_i.phase - gs_u.phase)
    return power_factor
