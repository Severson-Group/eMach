from .machine import Machine, MissingValueError
from .radial_machines import DPNVWinding_IM, IM_Rotor, Stator_IM, MachineComponent

__all__ = ['IM_Machine']


class IM_Machine(Machine, IM_Rotor, Stator_IM, DPNVWinding_IM):

    def __init__(self, machine_parameter_dict: dict, materials_dict: dict, nameplate_dict: dict) -> "IM_Machine":
        """ Creates a IM_Machine object
        Keyword Arguments:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
        Return Values
            machine: IM_Machine
        """
        cls = IM_Machine

        # first checks to see if the input dictionarys have the required values
        if cls.check_required_values(cls, machine_parameter_dict,
                                     materials_dict,
                                     nameplate_dict):
            setattr(self, '_machine_parameter_dict', machine_parameter_dict)
            setattr(self, '_materials_dict', materials_dict)
            setattr(self, '_nameplate_dict', nameplate_dict)

        else:
            # If required values are missing, collect them and raise execption
            missing_values = cls.get_missing_required_values(cls, machine_parameter_dict,
                                                             materials_dict,
                                                             nameplate_dict)
            raise (MissingValueError(missing_values,
                                     ('Missing inputs to initilize in' + str(cls))))

    def get_missing_required_values(cls, machine_geometry_dict: dict,
                                    materials_dict: dict,
                                    nameplate_dict: dict) -> list:
        """returns missing required values from input dictionary 
        
        Keyword Arguments:
            cls: Class
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
            nameplate_dict: dict
        Return Values
            missing_values: list
        """
        # missing_values = []
        # for a in [[cls.required_parameters(), machine_geometry_dict],
        #           [cls.required_materials(), materials_dict],
        #           [cls.required_nameplate(), nameplate_dict]]:
        #     for value in a[0]:
        #         if value in a[1]:
        #             pass
        #         else:
        #             missing_values.append(value)
        # return missing_values
        return None

    def check_required_values(cls, machine_geometry_dict: dict,
                              materials_dict: dict,
                              nameplate_dict: dict) -> bool:
        """Checks to see if input dictionary have required values
        
        Keyword Argumets:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
            nameplate_dict: dict
        Return Values
            bool
        """

        if not cls.get_missing_required_values(cls, machine_geometry_dict,
                                               materials_dict,
                                               nameplate_dict):
            return True
        else:
            return False

    def required_parameters():
        # return None
        req_geo=('Length_AirGap','l_st')
        for cl in IM_Machine.__bases__:
            if issubclass(cl, MachineComponent):
                if cl.required_parameters() is not None:
                    req_geo = req_geo + cl.required_parameters()
        return req_geo

    def required_materials():
        req_mat = ()
        for cl in IM_Machine.__bases__:
            if issubclass(cl, MachineComponent):
                if cl.required_materials() is not None:
                    req_mat = req_mat + cl.required_materials()
        return req_mat

    def required_nameplate():
        return ('mech_power'  # kW
                ,'Omega'  # rad/s
                ,'voltage_rating'  # Vrms (line-to-line, Wye-Connect)
                ,'Iq_rated_ratio'  # per rated coil currents
                ,'Rated_current'
                ,'Bar_Conductivity'
                ,'BeariW_CurrentAmp'
                ,'BeariW_Freq'
                ,'BeariW_Rs'
                ,'BeariW_poles'
                ,'BeariW_turns'
                ,'CurrentAmp_per_phase'
                ,'DriveW_CurrentAmp'
                ,'DriveW_Freq'
                ,'DriveW_Rs'
                ,'DriveW_poles'
                ,'DriveW_zQ'
                ,'End_Ring_Resistance'
                , 'Js'
                )

    @property
    def Length_AirGap(self):
        return self._machine_parameter_dict['Length_AirGap']

    @property
    def l_st(self):
        return self._machine_parameter_dict['stack_length']


    @property
    def Location_RotorBarCenter(self):
        return self._machine_parameter_dict['Location_RotorBarCenter']

    @property
    def Bar_Conductivity(self):
        return self._machine_parameter_dict['Bar_Conductivity']

    @property
    def BeariW_CurrentAmp(self):
        return self._machine_parameter_dict['BeariW_CurrentAmp']

    @property
    def BeariW_Freq(self):
        return self._machine_parameter_dict['BeariW_Freq']

    @property
    def BeariW_Rs(self):
        return self._machine_parameter_dict['BeariW_Rs']

    @property
    def DriveW_poles(self):
        return self._machine_parameter_dict['DriveW_poles']

    @property
    def BeariW_poles(self):
        return self._machine_parameter_dict['BeariW_poles']

    @property
    def BeariW_turns(self):
        return self._machine_parameter_dict['BeariW_turns']

    @property
    def CurrentAmp_per_phase(self):
        return self._machine_parameter_dict['CurrentAmp_per_phase']

    @property
    def DriveW_CurrentAmp(self):
        return self._machine_parameter_dict['DriveW_CurrentAmp']

    @property
    def mech_power(self):
        return self._nameplate_dict['mech_power']

    @property
    def mech_omega(self):
        return self._nameplate_dict['mech_omega']

    @property
    def voltage_rating(self):
        return self._nameplate_dict['voltage_rating']

    @property
    def Iq_rated_ratio(self):
        return self._nameplate_dict['Iq_rated_ratio']

    @property
    def Rated_current(self):
        return self._nameplate_dict['Rated_current']

