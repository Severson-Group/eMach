__all__ = ["SynR_Machine_Oper_Pt"]
import numpy as np

class SynR_Machine_Oper_Pt:
    """This is a wrapper class designed to contain all relevant information
    on the operating point for obtaining electrical performance evaluation of
    synchronous reluctance machines
    """

    def __init__(self, speed, speed_ratio, phi_0, ambient_temp, rotor_temp_rise,):
        """
        Args:
            speed: Machine rotational speed in RPM.
            speed_ratio: percent of speed being operated in decimal form.
            ambient_temp: ambient temperature in celsius.
            rotor_temp_rise: allowed rotor temperature rise in K.
            phi_0: current phase shift in deg.
        """

        self.__speed = speed
        self.__speed_ratio = speed_ratio
        self.__phi_0 = phi_0
        self.__ambient_temp = ambient_temp
        self.__rotor_temp_rise = rotor_temp_rise

    @property
    def speed(self):
        return self.__speed

    @property
    def speed_ratio(self):
        return self.__speed_ratio
    
    @property
    def phi_0(self):
        return self.__phi_0

    @property
    def ambient_temp(self):
        return self.__ambient_temp

    @property
    def rotor_temp_rise(self):
        return self.__rotor_temp_rise