import numpy as np

from .architect import Architect
from .machines import IM_Machine
from .winding_layout import WindingLayout

__all__ = ['IMArchitectType1']


class IMArchitectType1(Architect):
    '''
    This class acts as an interface between the end user and the IM_Machine class.
    Each Architect class has to be tailor made based on the expected free variables
    from the optimization algorithm
    
    '''

    def __init__(self, specification):
        '''
        Initializes the architecture with IM machine materials and design
        specifications.

        Parameters
        ----------
        specification : IMMachineSpec
            This is an object of the class IMMachineSpec.

        Returns
        -------
        None.

        '''
        self.__design_spec = specification.design_spec
        self.__rotor_material = specification.rotor_material
        self.__stator_material = specification.stator_material
        self.__coil_material = specification.coil_material
        self.__rotor_hub = specification.rotor_hub
        self.__air = specification.air
        self.__rotor_bar_material = specification.rotor_bar_material
        self.__shaft_material = specification.shaft_material
        self.__winding = WindingLayout(DPNV_or_SEPA=True, Qs=self.__design_spec['Q'], \
                                       p=self.__design_spec['p'])

    def create_new_design(self, x):
        '''
        Takes in a list of free variables from the optimization algorithm, 
        based on which the Machine class is instantiated.

        Parameters
        ----------
        x : List
            A list of free variables 

        Returns
        -------
        machine_variant : IM_Machine
            An instance of the IM_Machine class containing all information
            relevant to a bearingless synchronous permanent magnet motor.

        '''

        free_variables = self.x_to_dict(x)

        im_parameters = {

            'Qs': self.__design_spec['Q'],
            'Qr': self.__design_spec['Qr'],
            'Angle_StatorSlotSpan': 360 / self.__design_spec['Q'],
            'Angle_RotorSlotSpan': 360 / self.__design_spec['Qr'],

            'Radius_OuterStatorYoke': free_variables['Radius_OuterStatorYoke'],
            'Radius_InnerStatorYoke': free_variables['Radius_InnerStatorYoke'],
            'Length_AirGap'         : free_variables['delta_e'],
            'Radius_OuterRotor'     : free_variables['r_ro'],
            'Radius_Shaft'          : self.__get_r_sh(free_variables),

            'Length_HeadNeckRotorSlot': 1, #Jiahao is using 1 mm as default
            'Radius_of_RotorSlot': free_variables['Radius_of_RotorSlot'],
            'Location_RotorBarCenter': free_variables['Location_RotorBarCenter'],
            'Width_RotorSlotOpen': free_variables['Width_RotorSlotOpen'],

            # 'Radius_of_RotorSlot2': free_variables['Radius_of_RotorSlot2'],
            # 'Location_RotorBarCenter2': free_variables['Location_RotorBarCenter2'],

            #As of now no double bar rotor
            'Radius_of_RotorSlot2':0,
            'Location_RotorBarCenter2': 0,

            'Angle_StatorSlotOpen'          : self.__get_Angle_StatorSlotOpen,
            'Width_StatorTeethBody'         : free_variables['w_st'],
            'Width_StatorTeethHeadThickness': free_variables['d_so'],
            'Width_StatorTeethNeck'         : free_variables['d_so']*0.5,

            'DriveW_poles': self.__design_spec['p'],
            'DriveW_zQ': free_variables['DriveW_zQ'],
            'DriveW_Rs': free_variables['DriveW_Rs'],
            'DriveW_CurrentAmp': free_variables['DriveW_CurrentAmp'],
            'Width_StatorTeethHeadThickness': free_variables['Width_StatorTeethHeadThickness'],
            'Width_StatorTeethHeadThickness': free_variables['Width_StatorTeethHeadThickness'],
            'Width_StatorTeethHeadThickness': free_variables['Width_StatorTeethHeadThickness'],

            # dependant variables
            'alpha_so': self.__get_alpha_so(free_variables),
            'd_sp': self.__get_d_sp(free_variables),
            'r_si': self.__get_r_si(free_variables),
            'alpha_ms': self.__get_alpha_ms(free_variables),
            'd_ms': self.__get_d_ms(free_variables),
            'r_sh': self.__get_r_sh(free_variables),
            'r_so': self.__get_r_so(free_variables),
            's_slot': self.__get_s_slot(free_variables),
            'p': self.__design_spec['p'],
            'V_r': self.__get_V_r(free_variables),
            'l_st': self.__get_l_st(free_variables),
            'd_sl': 0.001,
            'delta_sl': 0,
            'delta': free_variables['delta_e'],
            'Q': self.__design_spec['Q'],
            'n_m': 1,

            # winding parameters
            'coil_groups': self.__winding.grouping_a,
            'no_of_layers': self.__winding.no_winding_layer,
            'layer_phases': [self.__winding.rightlayer_phase, self.__winding.leftlayer_phase],
            'layer_polarity': [self.__winding.rightlayer_polarity, self.__winding.leftlayer_polarity],
            'pitch': self.__winding.y,
            'Z_q': self.__get_zQ(free_variables),
            'Kov': self.__design_spec['Kov'],
            'Kcu': self.__design_spec['Kcu'],
        }

        im_material = {
            'air_mat': self.__air,
            'rotor_iron_mat': self.__rotor_material,
            'stator_iron_mat': self.__stator_material,
            'magnet_mat': self.__magnet_material,
            'rotor_sleeve_mat': self.__sleeve_material,
            'coil_mat': self.__coil_material,
            'shaft_mat': self.__shaft_material,
            'rotor_hub': self.__rotor_hub
        }

        im_nameplate = {

            'mech_omega': self.__design_spec['rated_speed'],
            'mech_power': self.__design_spec['rated_power'],
            'voltage_rating': self.__design_spec['voltage_rating'],
            'Iq_rated_ratio': 0.95,
            'Rated_current': self.__current_coil,
            'ps': self.__design_spec['ps'],
        }

        machine_variant = IM_Machine(im_parameters, im_material, im_nameplate)
        return machine_variant

    @property
    def __current_coil(self):
        I_hat = self.__design_spec['wire_A'] * self.__design_spec['J'] * 1.414
        return I_hat

    def __get_Radius_OuterStatorYoke(self, free_variables):
        r_si = self.__get_r_si(free_variables)
        d_sp = self.__get_d_sp(free_variables)
        d_st = free_variables['d_st']
        d_sy = free_variables['d_sy']
        return r_si + d_sp + d_st + d_sy

    def __get_Radius_InnerStatorYoke(self, free_variables):
        r_si = self.__get_r_si(free_variables)
        d_sp = self.__get_d_sp(free_variables)
        d_st = free_variables['d_st']
        return r_si + d_sp + d_st

    def __get_Angle_StatorSlotOpen(self):
        return 0.5 * (360 / self.__design_spec['Q'])

    def __turns_calculator(self):
        desired_emf_Em = 0.95 * self.__design_spec['stator_phase_voltage_rms'] # 0.96~0.98, high speed motor has higher leakage reactance hence 0.95
        ExcitationFreqSimulated = self.__design_spec['rated_speed']/60
        flux_linkage_Psi_m = 1.414*desired_emf_Em / (2*3.14*ExcitationFreqSimulated)
        return flux_linkage_Psi_m

    

    #
    #
    # def __get_d_sp(self, free_variables):
    #     d_so = free_variables['d_so']
    #     return 1.5*d_so
    #
    def __get_r_si(self, free_variables):
        delta_e = free_variables['delta_e']
        r_ro = free_variables['r_ro']
        return r_ro + delta_e

    #
    # def __get_alpha_ms(self, free_variables):
    #     alpha_m = free_variables['alpha_m']
    #     return alpha_m
    #
    # def __get_d_ms(self, free_variables):
    #     return 0
    #
    def __get_Radius_Shaft(self, free_variables):
        r_ro = free_variables['r_ro']
        d_ri = free_variables['d_ri']
        return r_ro - d_ri

    #
    # def __get_r_so(self, free_variables):
    #     r_si = self.__get_r_si(free_variables)
    #     d_sp = self.__get_d_sp(free_variables)
    #     d_st = free_variables['d_st']
    #     d_sy = free_variables['d_sy']
    #     return r_si + d_sp + d_st + d_sy
    #
    # def __get_s_slot(self, free_variables):
    #     r_si = self.__get_r_si(free_variables)
    #     d_sp = self.__get_d_sp(free_variables)
    #     w_st = free_variables['w_st']
    #     d_st = free_variables['d_st']
    #     return (np.pi/self.__design_spec['Q'])*((r_si+d_sp+d_st)**2 - (r_si+d_sp)**2) - w_st*d_st
    #
    # def __get_zQ(self, free_variables):
    #     s_slot = self.__get_s_slot(free_variables)
    #     Kcu    = self.__design_spec['Kcu']
    #     zQ = round(Kcu*s_slot/(2*self.__design_spec['wire_A']));
    #     return zQ
    #
    # def __get_l_st(self, free_variables):
    #     return 0.001
    #
    # def __get_V_r(self, free_variables):
    #     l_st = self.__get_l_st(free_variables)
    #     V_r = np.pi*free_variables['r_ro']**2*l_st
    #     return V_r
    #
    #
    # def __get_alpha_so(self, free_variables):
    #     alpha_so = free_variables['alpha_st']/2
    #     return alpha_so
    #
    # def __winding(self):
    #     x = self.__design_spec['Q']
    #     return x

    def x_to_dict(self, x):
        free_variables = {
            'delta_e': x[0],
            'r_ro': x[1],
            'alpha_st': x[2],
            'd_so': x[3],
            'w_st': x[4],
            'd_st': x[5],
            'd_sy': x[6],
            'alpha_m': x[7],
            'd_m': x[8],
            'd_mp': x[9],
            'd_ri': x[10],
        }
        return free_variables
