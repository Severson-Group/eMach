import numpy as np
import sys

from mach_eval.machines.SynR.AM_SynR_machine import AM_SynR_Machine


class AM_SynR_Architect:
    """
    This class acts as an interface between the end user and the AM_SynR_Machine class.
    Each Architect class has to be tailor made based on the expected free variables
    from the optimization algorithm
    """

    def __init__(self, AM_SynR_parameters, AM_SynR_materials, AM_SynR_winding):
        """
        Initializes the architecture with SynR machine materials and design
        specifications.

        Parameters
        ----------
        specification : AM_SynRMachineSpec
            This is an object of the class AM_SynRMachineSpec.

        Returns
        -------
        None.

        """
        self.__AM_SynR_parameters = AM_SynR_parameters
        self.__AM_SynR_materials = AM_SynR_materials
        self.__AM_SynR_winding = AM_SynR_winding
        # update below number to start from a particular project number for machine name
        # useful when resuming optimizations
        self.count = 0 

    def create_new_design(self, x):
        """
        Takes in a list of free variables from the optimization algorithm,
        based on which the Machine class is instantiated.

        Parameters
        ----------
        x : List
            A list of free variables

        Returns
        -------
        machine_variant : AM_SynR_Machine
            An instance of the AM_SynR_Machine class containing all information
            relavant to an additively manufactured synchronous reluctance motor.

        """
        self.count = self.count + 1   # update machine ID
        free_variables = self.x_to_dict(x)

        AM_SynR_dimensions = {
            "r_ri": free_variables["r_ri"],
            "r_ro": free_variables["r_ro"],
            "d_r1": free_variables["d_r1"],
            "d_r2": free_variables["d_r2"],
            "w_b1": free_variables["w_b1"],
            "w_b2": free_variables["w_b2"],
            # dependent variables
            "alpha_so": self.__get_alpha_so(),
            "alpha_st": self.__get_alpha_st(),
            "d_so": self.__get_d_so(),
            "d_sp": self.__get_d_sp(),
            "d_st": self.__get_d_st(),
            "d_sy": self.__get_d_sy(),
            "r_sh": self.__get_r_sh(free_variables),
            "r_si": self.__get_r_si(),
            "w_st": self.__get_w_st(),
            "l_st": self.__get_l_st(),
        }

        AM_SynR_parameters = {
            "p": self.__AM_SynR_parameters["p"],
            "Q": self.__AM_SynR_parameters["Q"],
            "rated_speed": self.__AM_SynR_parameters["rated_speed"],
            "rated_current": self.__AM_SynR_parameters["rated_current"],
            "name": "proj_" + str(self.count)
        }
        
        AM_SynR_winding = {
            "no_of_layers": self.__AM_SynR_winding["no_of_layers"],
            "layer_phases": self.__AM_SynR_winding["layer_phases"],
            "layer_polarity": self.__AM_SynR_winding["layer_polarity"],
            "pitch": self.__AM_SynR_winding["pitch"],
            "Z_q": self.__AM_SynR_winding["Z_q"],
            "Kov": self.__AM_SynR_winding["Kov"],
            "Kcu": self.__AM_SynR_winding["Kcu"],
            "phase_current_offset": self.__AM_SynR_winding["phase_current_offset"],
        }

        AM_SynR_materials = self.__AM_SynR_materials

        machine_variant = AM_SynR_Machine(
            AM_SynR_dimensions, AM_SynR_parameters, AM_SynR_materials, AM_SynR_winding
        )
        return machine_variant

    def __get_alpha_so(self):
        alpha_so = 3.75
        return alpha_so
    
    def __get_alpha_st(self):
        alpha_st = 7.5
        return alpha_st

    def __get_d_so(self):
        d_so = 1
        return d_so
    
    def __get_d_sp(self):
        d_sp = 2
        return d_sp
    
    def __get_d_st(self):
        d_st = 16.52
        return d_st
    
    def __get_d_sy(self):
        d_sy = 9.39
        return d_sy

    def __get_r_sh(self, free_variables):
        r_sh = free_variables["r_ri"]
        return r_sh
    
    def __get_r_si(self):
        r_si = 50.5
        return r_si
    
    def __get_w_st(self):
        w_st = 3.25
        return w_st
    
    def __get_l_st(self):
        l_st = 70.61
        return l_st

    def x_to_dict(self, x):
        free_variables = {
            "r_ri": x[0],
            "r_ro": x[1],
            "d_r1": x[2],
            "d_r2": x[3],
            "w_b1": x[4],
            "w_b2": x[5],
        }
        return free_variables