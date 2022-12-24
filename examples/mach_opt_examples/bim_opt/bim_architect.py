import numpy as np
import os
import sys

# change current working directory to file location
sys.path.append(os.path.dirname(__file__)+"/../../..")

from mach_eval.machines.bim import bim_machine as BIM_Machine
from mach_eval.machines.bspm.winding_layout import WindingLayout


class BIM_Architect:
    """
    This class acts as an interface between the end user and the BIM_Machine class.
    Each Architect class has to be tailor made based on the expected free variables
    from the optimization algorithm
    """

    def __init__(self, bim_parameters, bim_materials, bim_winding):
        """
        Initializes the architecture with BIM machine materials and design
        specifications.

        Parameters
        ----------
        specification : BIMMachineSpec
            This is an object of the class BIMMachineSpec.

        Returns
        -------
        None.

        """
        self.__bim_parameters = bim_parameters
        self.__bim_materials = bim_materials
        self.__bim_winding = bim_winding
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
        machine_variant : BIM_Machine
            An instance of the BIM_Machine class containing all information
            relavant to a bearingless induction motor.

        """
        self.count = self.count+1   # update machine ID
        free_variables = self.x_to_dict(x)

        bim_dimensions = {
            "alpha_st": free_variables["alpha_st"],
            "d_so": free_variables["d_so"],
            "d_st": free_variables["d_st"],
            "d_sy": free_variables["d_sy"],
            "w_st": free_variables["w_st"],  
            "d_rso": free_variables["d_rso"],
            "r_rb": free_variables["r_rb"],
            "w_so": free_variables["w_so"],
            # dependant variables
            "alpha_so": self.__get_alpha_so(free_variables),
            "r_si": self.__get_r_si(free_variables),        
            "d_sp": self.__get_d_sp(free_variables),
            "r_ri": 7.515,
            "d_ri": self.__get_d_ri(free_variables),
            "l_st": 1, #self.__get_l_st(free_variables),
        }

        bim_parameters = {
            "p": self.__bim_parameters["p"],
            "ps": self.__bim_parameters["ps"],
            "Q": self.__bim_parameters["Q"],
            "Qr": self.__bim_parameters["Qr"],
            "n_m": self.__bim_parameters["n_m"],
            "rated_speed": self.__bim_parameters["rated_speed"],
            "rated_power": self.__bim_parameters["rated_power"],
            "rated_voltage": self.__bim_parameters["voltage_rating"],
            "rated_current": self.__current_coil,
            "name": "proj_" + str(self.count) + "_"
        }
        
        # bim_winding = self.__bim_winding
        bim_winding = {
            "no_of_phases": self.__bim_winding["no_of_layers"],
            "no_of_layers": self.__bim_winding["no_of_layers"],
            "name_phases": self.__bim_winding["name_phases"],
            "layer_phases": self.__bim_winding["layer_phases"],
            "layer_polarity": self.__bim_winding["layer_polarity"],
            "pitch": self.__bim_winding["pitch"],
            "Z_q": self.__get_zQ(free_variables),
            "Kov": self.__bim_winding["Kov"],
            "Kcu": self.__bim_winding["Kcu"],
            "phase_current_offset": self.__bim_winding["phase_current_offset"],
            "no_of_layers_rotor": self.__bim_winding["no_of_layers_rotor"],
            "name_phases_rotor": self.__bim_winding["name_phases_rotor"],
            "layer_phases_rotor": self.__bim_winding["layer_phases_rotor"],
            "layer_polarity_rotor": self.__bim_winding["layer_polarity_rotor"],
            "Z_q_rotor": self.__bim_winding["Z_q_rotor"],
            'no_of_phases_rotor': self.__bim_winding["no_of_phases_rotor"],
            "Kov_rotor": self.__bim_winding["Kov_rotor"],
        }

        bim_materials = self.__bim_materials

        machine_variant = BIM_Machine(
            bim_dimensions, bim_parameters, bim_materials, bim_winding
        )
        return machine_variant

    @property
    def __current_coil(self):
        I_rms = self.__bim_parameters["wire_area"] * self.__bim_parameters["J"]
        return I_rms

    @property
    def r_ro(self):
        v = self.__bim_parameters['rated_speed_m_s']
        omega_m = self.__bim_parameters['rated_speed'] / 60 * 2 * np.pi
        r_ro = v / omega_m
        return r_ro

    def __get_alpha_so(self, free_variables):
        alpha_so = free_variables["alpha_st"] / 2
        return alpha_so

    def __get_r_si(self, free_variables):
        return (self.r_ro + free_variables["delta_e"])

    def __get_d_sp(self, free_variables):
        d_so = free_variables["d_so"]
        return 1.5 * d_so

    # def __get_r_ri(self, free_variables):
    #     r_ri = 0
    #     return r_ri

    def __get_d_ri(self, free_variables):
        r_ro = self.r_ro
        w_so = free_variables["w_so"]
        r_rb = free_variables["r_rb"]
        d_rso = free_variables["d_rso"]
        r_ri = free_variables["r_ri"]

        d_ri = (
            np.sqrt(r_ro ** 2 - (w_so / 2) ** 2) - 
            d_rso - np.sqrt(r_rb ** 2 - (w_so / 2) ** 2 ) - 
            r_rb - r_ri
        )
        return d_ri

    # def __get_r_rb(self, free_variables):
    #     return r_rb

    # def __get_l_st(self, free_variables):
    #     return 1

    def s_slot(self, free_variables):
        r_si = self.__get_r_si(free_variables)
        d_sp = self.__get_d_sp(free_variables)
        w_st = free_variables["w_st"]
        d_st = free_variables["d_st"]
        return (np.pi / self.__bim_parameters["Q"]) * (
            (r_si + d_sp + d_st) ** 2 - (r_si + d_sp) ** 2
        ) - w_st * d_st

    def __get_zQ(self, free_variables):
        s_slot = self.s_slot(free_variables)
        Kcu = self.__bim_parameters["Kcu"]
        zQ = round(Kcu * s_slot * 1e-6 / (2 * self.__bim_parameters["wire_area"]))
        if zQ < 1:
            zQ = 1
        return zQ


    # def x_to_dict(self, x):
    #     free_variables = {
    #         "delta_e": x[0],
    #         "w_st": x[1],
    #         "w_rt": x[2],
    #         "alpha_st": x[3],
    #         "alpha_rt": x[4],
    #         "d_so": x[5],
    #         "d_rso": x[6],
    #         "d_st": x[7],
    #         "d_sy": x[8],
    #     }
    #     return free_variables

    def x_to_dict(self, x):
        free_variables = {
            "delta_e": x[0],
            "w_st": x[1],
            "alpha_st": x[2],
            "d_so": x[3],
            "d_st": x[4],
            "d_sy": x[5],
            "r_rb": x[6],
            "w_so": x[7],
            "d_rso": x[8],
        }
        return free_variables
