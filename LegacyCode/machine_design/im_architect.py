import numpy as np

from .architect import Architect
from .machines import IM_Machine
from .winding_layout_im import winding_layout_v2
import numpy as np

from specifications.machine_specs.im1_machine_specs import DesignSpec

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
        # self.__winding = winding_layout_v2(DPNV_or_SEPA=True, Qs=self.__design_spec['Q'], \
        #                                p=self.__design_spec['p'], ps = self.__design_spec['ps'],\
        #                                    coil_pitch_y= (0.5*self.__design_spec['Q'])/self.__design_spec['p'])

        self.__winding = winding_layout_v2(DPNV_or_SEPA=True, Qs=24, \
                                       p=3, ps = 4,\
                                           coil_pitch_y= 3)

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

            'Qs': self.__design_spec['Qs'],
            'Qr': self.__design_spec['Qr'],
            'Angle_StatorSlotSpan': 360/self.__design_spec['Qs'],
            'Angle_RotorSlotSpan': 360/self.__design_spec['Qr'],

            'Radius_OuterStatorYoke': free_variables['Radius_OuterStatorYoke'],
            'Radius_InnerStatorYoke': free_variables['Radius_InnerStatorYoke'],
            'Length_AirGap': free_variables['Length_AirGap'],
            'Radius_OuterRotor': free_variables['Radius_OuterRotor'],
            'Radius_Shaft': free_variables['Radius_Shaft'],

            'Length_HeadNeckRotorSlot': free_variables['Length_HeadNeckRotorSlot'],  # Jiahao is using 1 mm as default
            'Radius_of_RotorSlot': free_variables['Radius_of_RotorSlot'],
            'Location_RotorBarCenter': free_variables['Location_RotorBarCenter'],
            'Width_RotorSlotOpen': free_variables['Width_RotorSlotOpen'],

            # 'Radius_of_RotorSlot2': free_variables['Radius_of_RotorSlot2'],
            # 'Location_RotorBarCenter2': free_variables['Location_RotorBarCenter2'],

            # As of now no double bar rotor
            'Radius_of_RotorSlot2': free_variables['Radius_of_RotorSlot2'],
            'Location_RotorBarCenter2': free_variables['Location_RotorBarCenter2'],

            'Angle_StatorSlotOpen': free_variables['Angle_StatorSlotOpen'],
            'Width_StatorTeethBody': free_variables['Width_StatorTeethBody'],
            'Width_StatorTeethHeadThickness': free_variables['Width_StatorTeethHeadThickness'],
            'Width_StatorTeethNeck': free_variables['Width_StatorTeethNeck'],

            'DriveW_poles':  2*self.__design_spec['p'],
            'DriveW_zQ': 10,

            # Not going to consider resistance for now
            # 'DriveW_Rs': free_variables['DriveW_Rs'],

            'DriveW_CurrentAmp': 127.89733,
            'DriveW_CurrentAmpUsed': 127.89733 * 0.975,
            'BeariW_CurrentAmpUsed': 127.89733 * 0.025,
            'DriveW_Freq': 500,

            'Bar_Conductivity' : 47619047.61904761,
            'stack_length': free_variables['stack_length'],

            'BeariW_poles': 2*self.__design_spec['ps'],

            'BeariW_turns': 10,

            'coil_groups': self.__winding.grouping_AC,
            'no_of_layers': self.__winding.number_winding_layer,
            'layer_phases': [self.__winding.layer_X_phases, self.__winding.layer_Y_phases],
            'layer_polarity': [self.__winding.layer_X_signs, self.__winding.layer_Y_signs],
            'pitch': self.__winding.coil_pitch_y,
            'use_drop_shape_rotor_bar': self.__design_spec['use_drop_shape_rotor_bar'],
            'PoleSpecificNeutral': self.__design_spec['PoleSpecificNeutral'],
            'number_parallel_branch': self.__design_spec['number_parallel_branch'],
            'DPNV_or_SEPA': self.__design_spec['DPNV_or_SEPA'],
            'CommutatingSequenceD': self.__winding.CommutatingSequenceD

        }

        im_material = {
            'air_mat': self.__air,
            'rotor_iron_mat': self.__rotor_material,
            'stator_iron_mat': self.__stator_material,
            'rotor_bar_mat': self.__rotor_bar_material,
            'coil_mat': self.__coil_material,
            'shaft_mat': self.__shaft_material,
            'rotor_hub': self.__rotor_hub
        }

        im_nameplate = {

            'mech_omega': self.__design_spec['rated_speed'],
            'mech_power': self.__design_spec['rated_power'],
            'voltage_rating': self.__design_spec['voltage_rating'],
            'Iq_rated_ratio': 0.975,
            'Rated_current': im_parameters['DriveW_CurrentAmp'],
            'ps': self.__design_spec['ps'],
        }

        machine_variant = IM_Machine(im_parameters, im_material, im_nameplate)
        return machine_variant

    @property
    def __get_current_coil(self):
        stator_phase_current_rms = self.__design_spec['rated_power'] / (\
                    self.__design_spec['m']  \
                    * 0.96 \
                    * self.__design_spec['voltage_rating'] \
                    * 0.9)
        return stator_phase_current_rms

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

    def __get_r_sh(self, free_variables):
        return free_variables['d_ri']*0.5

    @property
    def __get_Angle_StatorSlotOpen(self):
        Angle_StatorSlotOpen = 0.5 * (360 / self.__design_spec['Q'])
        print('Angle Stator slot open', Angle_StatorSlotOpen)
        return Angle_StatorSlotOpen

    def __get_pole_pitch_tau_p(self, free_variables):
        air_gap_diameter_D = free_variables['Length_AirGap'] + 2*free_variables['Radius_OuterRotor']
        return np.pi * air_gap_diameter_D / (2 * self.__design_spec['p'])


    def __get_turns(self, free_variables):

        desired_emf_Em = 0.95 * self.__design_spec['voltage_rating'] # 0.96~0.98, high speed motor has higher leakage reactance hence 0.95

        alpha_i = 2 / 3.14 # ideal sinusoidal flux density distribusion, when the saturation happens in teeth, alpha_i becomes higher.
        air_gap_flux_Phi_m = alpha_i * self.__design_spec['guess_air_gap_flux_density'] * self.__get_pole_pitch_tau_p(free_variables)\
                             * self.__get_l_st
        ExcitationFreqSimulated = self.__design_spec['ExcitationFreqSimulated']
        no_series_coil_turns_N = np.round(np.sqrt(2) * desired_emf_Em / (2 * np.pi * ExcitationFreqSimulated\
                                                                         * self.__design_spec['kw1'] * air_gap_flux_Phi_m))

        if self.__design_spec['DPNV_or_SEPA'] == True:
            number_parallel_branch = 2
        else:
            number_parallel_branch = 1
            # print('\n''In some cases, eselfially in low-voltage, high-power machines, there may be a need to change the stator slot number, the number of parallel paths or even the main dimensions of the machine in order to find the appropriate number of conductors in a slot.''')
        no_conductors_per_slot_zQ = 2 * 3 * no_series_coil_turns_N / self.__design_spec['Qs'] * number_parallel_branch
        # 3 here is number of phases please change this by adding the machine specification (check bp1_machine_spec)
        return no_conductors_per_slot_zQ








    #
    #
    def __get_d_sp(self, free_variables):
        d_so = free_variables['d_so']
        return 1.5*d_so
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
    @property
    def __get_l_st(self):
        return 0.001*1000
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
            'Radius_OuterStatorYoke': x[0],
            'Radius_InnerStatorYoke': x[1],
            'Length_AirGap': x[2],
            'Radius_OuterRotor': x[3],
            'Radius_Shaft': x[4],
            'Length_HeadNeckRotorSlot': x[5],
            'Radius_of_RotorSlot': x[6],
            'Location_RotorBarCenter': x[7],
            'Width_RotorSlotOpen': x[8],
            'Radius_of_RotorSlot2': x[9],
            'Location_RotorBarCenter2': x[10],
            'Angle_StatorSlotOpen'   : x[11],
            'Width_StatorTeethBody'  : x[12],
            'Width_StatorTeethHeadThickness' : x[13],
            'Width_StatorTeethNeck'     : x[14],
            'stack_length'  : x[15]

        }
        return free_variables
