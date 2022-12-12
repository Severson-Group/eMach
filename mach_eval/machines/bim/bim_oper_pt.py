__all__ = ["BIM_Machine_Oper_Pt"]
import numpy as np

class BIM_Machine_Oper_Pt:
    """This is a wrapper class designed to contain all relevant information
    on the operating point for obtaining electrical performance evaluation of
    bearingless induction machines
    """

    def __init__(
        self,
        speed=150000,
        slip_freq=1,
        It_hat=0,
        Is_hat = 0,
        phi_t_0 = 0,
        phi_s_0 = 0,
        ambient_temp=25,
        rotor_temp_rise=55,
    ):
        """
        Args:
            speed: Machine rotational speed in RPM.
            slip_freq: Machine slip frequency in Hz.
            ambient_temp: ambient temperature in celsius.
            rotor_temp_rise: allowed rotor temperature rise in K
            I_t_hat: amplitude of torque current in A
            I_s_hat: amplitude of suspension current in A
            phi_t_0: torque current phase shift in deg. For example, phase 1: i_t_1 = I_t_hat * cos(2pift - phi_t_0)
            phi_s_0: torque current phase shift in deg. For example, phase 1: i_s_1 = I_s_hat * cos(2pift - phi_s_0)

        """

        self.__speed = speed
        self.__slip_freq = slip_freq
        self.__It_hat = It_hat
        self.__Is_hat = Is_hat
        self.__phi_t_0 = phi_t_0
        self.__phi_s_0 = phi_s_0
        self.__ambient_temp = ambient_temp
        self.__rotor_temp_rise = rotor_temp_rise

    @property
    def speed(self):
        return self.__speed

    @property
    def slip_freq(self):
        return self.__slip_freq

    @property
    def It_hat(self):
        return self.__It_hat

    @property
    def Is_hat(self):
        return self.__Is_hat

    @property
    def phi_t_0(self):
        return self.__phi_t_0

    @property
    def phi_s_0(self):
        return self.__phi_s_0

    @property
    def ambient_temp(self):
        return self.__ambient_temp

    @property
    def rotor_temp_rise(self):
        return self.__rotor_temp_rise