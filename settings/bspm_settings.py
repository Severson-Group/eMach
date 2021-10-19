# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:37:05 2021

@author: Bharat
"""

class BSPM_EMAnalyzer_Settings():
    """ This is a wrapper class designed to contain all relevant information
    on the operating point for obtaining electrical performance evaluation of
    bearingless permanent magnet electric machines
    """
    def __init__(self, Id, Iq, Ix, Iy, speed, ambient_temp, rotor_temp_rise):
        """
        Parameters
        ----------
        Id : float
            PU value of d-axis current.
        Iq : float
            PU value of q-axis current.
        Ix : float
            PU value of x-axis current.
        Iy : float
            PU value of y-axis current.
        speed : float
            Machine rotational speed in rad/s.
        ambient_temp : float
            Magnet temperature in celsius.

        Returns
        -------
        None.
        """
        
        self.__Id = Id
        self.__Iq = Iq
        self.__Ix = Ix
        self.__Iy = Iy
        self.__speed = speed
        self.__ambient_temp = ambient_temp
        self.__rotor_temp_rise = rotor_temp_rise

    @property
    def Id(self):
        return self.__Id

    @property
    def Iq(self):
        return self.__Iq

    @property
    def Ix(self):
        return self.__Ix

    @property
    def Iy(self):
        return self.__Iy

    @property
    def speed(self):
        return self.__speed

    @property
    def magnet_temp(self):
        return self.__magnet_temp

    @property
    def ambient_temp(self):
        return self.__ambient_temp

    @property
    def rotor_temp_rise(self):
        return self.__rotor_temp_rise

    