from .machine import Machine, MissingValueError
from .radial_machines import DPNVWinding, PM_Rotor_Sleeved, Stator, MachineComponent
from copy import deepcopy

__all__ = ['BSPM_Machine']


class BSPM_Machine(Machine, PM_Rotor_Sleeved, Stator, DPNVWinding):

    def __init__(self, machine_parameter_dict: dict, materials_dict: dict, nameplate_dict: dict):
        """ Creates a BSPM_Machine object
        Keyword Argumets:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
        Return Values
            machine: BSPM_Machine 
        """
        cls = BSPM_Machine

        # first checks to see if the input dictionarys have the required values

        if cls.check_required_values(cls, machine_parameter_dict, materials_dict, nameplate_dict) == True:
            setattr(self, '_machine_parameter_dict', machine_parameter_dict)
            setattr(self, '_materials_dict', materials_dict)
            setattr(self, '_nameplate_dict', nameplate_dict)

        else:
            # If required values are missing, collect them and raise execption
            missing_values = cls.get_missing_required_values(cls, machine_parameter_dict, materials_dict,
                                                             nameplate_dict)
            raise (MissingValueError(missing_values, ('Missing inputs to initialize in' + str(cls))))

    def get_missing_required_values(cls, machine_geometry_dict: dict, materials_dict: dict,
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

    def check_required_values(cls, machine_geometry_dict: dict, materials_dict: dict, nameplate_dict: dict) -> bool:
        """Checks to see if input dictionary have required values
        
        Keyword Argumets:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
            nameplate_dict: dict
        Return Values
            bool
        """
        if not cls.get_missing_required_values(cls, machine_geometry_dict, materials_dict, nameplate_dict):
            return True
        else:
            return False

    @staticmethod
    def required_parameters():
        req_geo = ('delta_e', 'delta', 'l_st')
        for cl in BSPM_Machine.__bases__:
            if issubclass(cl, MachineComponent):
                if cl.required_parameters() is not None:
                    req_geo = req_geo + cl.required_parameters()
        return req_geo

    @staticmethod
    def required_materials():
        req_mat = ()
        for cl in BSPM_Machine.__bases__:
            if issubclass(cl, MachineComponent):
                if cl.required_materials() is not None:
                    req_mat = req_mat + cl.required_materials()
        return req_mat

    @staticmethod
    def required_nameplate():
        return ('mech_power',  # kW
                'mech_omega',  # rad/s
                'voltage_rating',  # Vrms (line-to-line, Wye-Connect)
                'Rated_current',
                'ps',
                )

    def clone(self, **kwargs) -> 'BSPM_Machine':
        """Creates a clone of the machine with updated parameters using *kwars.

        Args:
            **kwargs: Machine dictionary to be updated.
        Returns:
            Cloned BSPM_Machine object.
        """
        cloned_machine = deepcopy(self)
        for dict_to_update, updated_values in kwargs.items():
            if dict_to_update == 'machine_parameter_dict':
                for key, value in updated_values.items():
                    cloned_machine._machine_parameter_dict[key] = value

            if dict_to_update == 'nameplate_dict':
                for key, value in updated_values.items():
                    cloned_machine._nameplate_dict[key] = value

            if dict_to_update == 'materials_dict':
                for key, value in updated_values.items():
                    cloned_machine._materials_dict[key] = value
        return cloned_machine

    @property
    def delta_e(self):
        return self._machine_parameter_dict['delta_e']

    @property
    def delta(self):
        return self._machine_parameter_dict['delta']

    @property
    def l_st(self):
        return self._machine_parameter_dict['l_st']

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
    def Rated_current(self):
        return self._nameplate_dict['Rated_current']

    @property
    def ps(self):
        return self._nameplate_dict['ps']
