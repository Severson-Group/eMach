from .machine import Machine, MissingValueError
from .radial_machines import DPNVWinding, IM_Rotor, Stator, MachineComponent

__all__ = ['IM_Machine']


class IM_Machine(Machine, IM_Rotor, Stator, DPNVWinding):

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
        missing_values = []
        for a in [[cls.required_parameters(), machine_geometry_dict],
                  [cls.required_materials(), materials_dict],
                  [cls.required_nameplate(), nameplate_dict]]:
            for value in a[0]:
                if value in a[1]:
                    pass
                else:
                    missing_values.append(value)
        return missing_values

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
        req_geo=('delta_e','delta','l_st')
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
        return ('mech_power',  # kW
                'mech_omega',  # rad/s
                'voltage_rating',  # Vrms (line-to-line, Wye-Connect)
                'Iq_rated_ratio',  # per rated coil currents
                'Rated_current',
                'ps'
                )

    @property
    def Length_AirGap(self):
        return self._machine_parameter_dict['Length_AirGap']

    @property
    def Radius_OuterStatorYoke(self):
        return self._machine_parameter_dict['Radius_OuterStatorYoke']

    @property
    def Radius_InnerStatorYoke(self):
        return self._machine_parameter_dict['Radius_InnerStatorYoke']

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

    @property
    def ps(self):
        return self._nameplate_dict['ps']
