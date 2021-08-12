import copy
import numpy as np


class BSPM_EM_PostAnalyzer():
    def copper_loss(self):
        return 6 * ((self.current_trms / 2) ** 2 + self.current_srms ** 2) * self.R_coil

    def get_next_state(results, in_state):
        state_out = copy.deepcopy(in_state)
        machine = state_out.design.machine

        ##############################################################################
        ############################ extract useful info ###########################
        ##############################################################################
        length = results['current'].shape[0]
        i = length - results['range_fine_step']
        results['current'] = results['current'].iloc[i:]

        results['torque'] = results['torque'].iloc[i:]
        results['force'] = results['force'].iloc[i:]
        results['voltage'] = results['voltage'].iloc[i:]
        results['hysterisis_loss'] = results['hysterisis_loss']
        results['iron_loss'] = results['iron_loss']
        results['eddy_current_loss'] = results['eddy_current_loss'].iloc[i:]

        ##############################################################################
        ############################ calculating volumes ###########################
        ##############################################################################
        # volumes = {}
        # # shaft volume
        # machine = state_out.design.machine
        # r_sh = machine.r_sh
        # l_st = machine.l_st
        # volumes['V_sh'] = np.pi*(r_sh**2)*l_st

        # # rotor iron volume
        # r_ro    = machine.r_ro
        # alpha_m = machine.alpha_m*np.pi/180
        # d_m     = machine.d_m
        # d_mp    = machine.d_mp
        # p       = machine.p
        # volumes['V_rfe'] = np.pi*((r_ro-d_m)**2-r_sh**2)*l_st + (np.pi - p*alpha_m)*((r_ro-d_mp)**2 - 
        # (r_ro-d_m)**2)*l_st

        # # magnet volume
        # volumes['V_rpm'] = p*alpha_m*(r_ro**2 - (r_ro-d_m)**2)*l_st

        # # sleeve volume
        # d_sl    = machine.d_sl
        # volumes['V_rsl'] = np.pi*((r_ro+d_sl)**2 - r_ro**2)*l_st

        # # Copper volume
        # s_slot = machine.s_slot
        # V_scu = machine.Q * self.l_coil * machine.Kcu * machine.s_slot /machine.no_of_layers

        # r_so    = machine.r_so
        # r_si    = machine.r_si
        # volumes['V_sfe'] = np.pi*(r_so**2 - r_si**2)*l_st - 6*s_slot*l_st

        ##############################################################################
        ############################ post processing #################################
        ##############################################################################
        torque_avg, torque_ripple = process_torque_data(results['torque'])
        f_x, f_y, force_avg, Em, Ea = process_force_data(results['force'])

        post_processing = {}
        post_processing['torque_avg'] = torque_avg
        post_processing['torque_ripple'] = torque_ripple

        post_processing['Fx'] = f_x
        post_processing['Fy'] = f_y
        post_processing['force_avg'] = force_avg
        post_processing['Em'] = Em
        post_processing['Ea'] = Ea

        post_processing['copper_loss'] = results['copper_loss']
        post_processing['rotor_iron_loss'] = results['iron_loss']['NotchedRotor'][0] \
                                             + results['eddy_current_loss']['NotchedRotor'].mean()
        post_processing['stator_iron_loss'] = results['iron_loss']['StatorCore'][0] \
                                              + results['eddy_current_loss']['StatorCore'].mean()
        post_processing['magnet_loss'] = results['eddy_current_loss']['Magnet'].mean()

        post_processing['phase_voltage_rms'] = compute_vrms(results['voltage'])
        post_processing['power_factor'] = compute_power_factor(results['voltage'], results['current'],
                                                               target_freq=machine.mech_omega * machine.p / (2 * np.pi))

        state_out.conditions.em = post_processing
        return state_out


def process_torque_data(torque_df):
    torque = torque_df['TorCon']
    avg_torque = torque.mean()
    torque_error = torque - avg_torque
    ss_max_torque_error = max(torque_error), min(torque_error)
    torque_ripple = abs(ss_max_torque_error[0] - ss_max_torque_error[1]) / avg_torque
    return avg_torque, torque_ripple


def compute_angle_error(alpha_star, alpha_actual):
    N = alpha_star.shape[0]  # determine number of input angles
    vectors_star = np.zeros((N, 2))
    vectors = np.zeros((N, 2))
    # unit vectors for desired angle
    vectors_star[:, 0] = np.cos(np.deg2rad(alpha_star))
    vectors_star[:, 1] = np.sin(np.deg2rad(alpha_star))
    # unit vectors for actual angle
    vectors[:, 0] = np.cos(np.deg2rad(alpha_actual))
    vectors[:, 1] = np.sin(np.deg2rad(alpha_actual))
    # determine angle between vectors in degrees (note that this is only the angle magnitude):
    # This is just doing the cross product between all corresponding unit vectors
    error_angle_mag = np.rad2deg(np.arccos((vectors_star * vectors).sum(axis=1)))
    # to determine the error angle direction we can use the cross product between the vectors
    # positive cross product means the desired vector lags the actual vector and the error angle
    # is positive
    sign = np.sign(np.cross(vectors_star, vectors))
    return sign * error_angle_mag


def process_force_data(force_df):
    force_x = np.asarray(force_df[r'ForCon:1st'])
    force_y = np.asarray(force_df[r'ForCon:2nd'])
    # correct JMAG offset
    theta_offset = -np.pi / 2
    force = (force_x + 1j * force_y) * np.exp(1j * theta_offset)
    force_x = np.real(force).tolist()
    force_y = np.imag(force).tolist()
    force_df[r'ForCon:1st'] = force_x
    force_df[r'ForCon:2nd'] = force_y
    # force magnitude and angle
    force_ang = []
    temp_force_ang = np.arctan2(force_y, force_x) / np.pi * 180  # [deg]
    for angle in temp_force_ang:
        force_ang.append(angle)
    force_abs = np.sqrt(np.array(force_x) ** 2 + np.array(force_y) ** 2)
    # average force
    force_average_angle = sum(force_ang) / len(force_ang)
    f_x = sum(force_x) / len(force_x)
    f_y = sum(force_y) / len(force_y)
    force_avg_magnitude = sum(force_abs) / len(force_abs)
    # Error magnitude
    force_err_abs = (force_abs - force_avg_magnitude) / force_avg_magnitude
    Em = max(abs(force_err_abs))
    # error angle
    force_err_ang = compute_angle_error(np.ones(len(force_ang)) * force_average_angle, np.array(force_ang))
    Ea = max(abs(force_err_ang))

    return f_x, f_y, force_avg_magnitude, Em, Ea


def compute_vrms(voltage_df):
    phase_voltage = voltage_df['Terminal_Wt']
    rms_voltage = np.sqrt(sum(np.square(phase_voltage)) / len(phase_voltage))
    return rms_voltage


def compute_power_factor(voltage_df, current_df, target_freq, numPeriodicalExtension=1000):
    mytime = current_df.index
    voltage = voltage_df['Terminal_Wt']
    current = current_df['coil_Wb']

    power_factor = compute_power_factor_from_half_period(voltage, current, mytime, targetFreq=target_freq,
                                                         numPeriodicalExtension=numPeriodicalExtension)
    return power_factor


# https://dsp.stackexchange.com/questions/11513/estimate-frequency-and-peak-value-of-a-signals-fundamental
# define N_SAMPLE ((long int)(1.0/(0.1*TS))) // Resolution 0.1 Hz = 1 / (N_SAMPLE * TS)


class GoertzelDataStruct(object):
    """docstring for GoertzelDataStruct"""

    def __init__(self, id=None, ):
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
                'This is for real time implementation of Goertzel, hence data must be a scalar rather than array.')

        if not gs.bool_initialized:
            gs.bool_initialized = True

            gs.count = 0
            gs.k = (0.5 + ((numSamples * targetFreq) / samplingRate))
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
        gs.q1 = q0  # // q1 is the newest output vk[N], while q2 is the last output vk[N-1].

        gs.accumSquaredData += data * data

        gs.count += 1
        if gs.count >= numSamples:
            # // calculate the real and imaginary results with scaling appropriately
            gs.real = (gs.q1 * gs.cosine - gs.q2) / gs.scalingFactor  # // inspired by the python script of sebpiq
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
            gs.k = (0.5 + ((numSamples * targetFreq) / samplingRate))
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
                gs.real = (gs.q1 * gs.cosine - gs.q2) / gs.scalingFactor  # // inspired by the python script of sebpiq
                gs.imag = (gs.q1 * gs.sine) / gs.scalingFactor

                # // reset
                gs.bool_initialized = False
                return True
        return None


def compute_power_factor_from_half_period(voltage, current, mytime, targetFreq=1e3,
                                          numPeriodicalExtension=1000):  # 目标频率默认是1000Hz

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

    gs_u.goertzel_offline(targetFreq, 1. / TS, voltage)
    gs_i.goertzel_offline(targetFreq, 1. / TS, current)

    gs_u.ampl = np.sqrt(gs_u.real * gs_u.real + gs_u.imag * gs_u.imag)
    gs_u.phase = np.arctan2(gs_u.imag, gs_u.real)

    gs_i.ampl = np.sqrt(gs_i.real * gs_i.real + gs_i.imag * gs_i.imag)
    gs_i.phase = np.arctan2(gs_i.imag, gs_i.real)

    phase_difference_in_deg = ((gs_i.phase - gs_u.phase) / np.pi * 180)
    power_factor = np.cos(gs_i.phase - gs_u.phase)
    return power_factor
