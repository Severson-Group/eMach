# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 09:36:01 2021

@author: Martin Johnson
"""
from machine import Machine,MissingValueError


class RadialMachine(Machine):
    """Parent Class for all radial machine topologies"""
    required_geometry={}
    required_materials={"stator_mat":None,"winding_mat":None}
    required_winding={} 
    required_nameplate={}
    
    def __init__(self,machine_geometry_dict:dict,materials_dict:dict,
                 winding_dict:dict,nameplate_dict:dict,
                 cls=None)->"RadialMachine":
        """ Creates a RadialMachine object
        Keyword Argumets:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
            cls: Class
        Return Values
            radial_machine: RadialMachine 
        """
        if cls==None:
            cls=RadialMachine
        
        #first checks to see if the input dictionarys have the required values
        if cls.check_for_required_values(cls,machine_geometry_dict,
                                              materials_dict,
                                              winding_dict,
                                              nameplate_dict)== True:
            #Add the machine geometry to the machine object
            for key in machine_geometry_dict.keys():
                private_key='_'+key
                setattr(self, private_key,machine_geometry_dict[key]) 
            #Add the machine materials to the machine object
            for key in materials_dict.keys():
                private_key='_'+key
                setattr(self, private_key,materials_dict[key])
            #Add the machine winding to the machine object
            for key in winding_dict.keys():
                private_key='_'+key
                setattr(self, private_key,winding_dict[key])
            self.machine_geometry_dict=machine_geometry_dict
            self.materials_dict=materials_dict
            self.winding_dict=winding_dict
            self.nameplate_dict=nameplate_dict
        else:
            #If required values are missing, collect them and raise execption
            missing_values=cls.get_missing_required_values(cls,machine_geometry_dict,
                                                                     materials_dict,
                                                                     winding_dict,
                                                                     nameplate_dict)
            raise(MissingValueError(missing_values,
                                    ('Missing inputs to initilize in'+str(cls))))
        
    def get_missing_required_values(cls,machine_geometry_dict:dict,
                                              materials_dict:dict,
                                              winding_dict:dict,
                                              nameplate_dict:dict)->list:
        """returns missing requried values from input dictionary 
        
        Keyword Argumets:
            cls: Class
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
            nameplate_dict: dict
        Return Values
            missing_values: list
        """
        missing_values=[]
        for d in [[cls.required_geometry,machine_geometry_dict],
                  [cls.required_materials,materials_dict],
                  [cls.required_winding,winding_dict],
                  [cls.required_nameplate,nameplate_dict]]:
            for key in d[0] :
                if key in d[1]:
                    pass
                else:
                    missing_values.append(key)
        return missing_values
    
    def get_required_values(cls):
        """Reuturns Dicts of requried values for class"""
        return {"required_geometry":cls.required_geometry,
                "required_materials":cls.required_materials,
                "required_winding":cls.required_winding,
                "required_nameplate":cls.required_nameplate}
    def check_for_required_values(cls,machine_geometry_dict:dict,
                                              materials_dict:dict,
                                              winding_dict:dict,
                                              nameplate_dict:dict)->bool:
        """Checks to see if input dictionary have required values
        
        Keyword Argumets:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
            nameplate_dict: dict
        Return Values
            bool
        """
        
        if cls.get_missing_required_values(cls,machine_geometry_dict,
                                              materials_dict,
                                              winding_dict,
                                              nameplate_dict)==[]:
            return True
        else:
            return False
    
class BSPM_Machine_2D(RadialMachine):
    """Bearingless Surface Mounted PM Machine Class. 
    This is a sub class of the RadialMachine class"""
    
    required_geometry={**RadialMachine.required_geometry,
                       **{'delta_e'      : None,#Effective Airgap
                          'r_ro'         : None,#Rotor Outer Radius
                          'alpha_st'     : None,#Stator Tooth Angle
                          'd_so'         : None,#Stator 
                          'w_st'         : None,#Stator Tooth Width
                          'd_st'         : None,#Stator Tooth Length
                          'd_sy'         : None,#Stator Yoke width
                          'alpha_m'      : None,#Magnet Segment Angle
                          'd_m'          : None,#Magnet Thickness
                          'd_mp'         : None,#Magnet 
                          'd_ri'         : None,#Rotor Outer Radius
                          'alpha_so'     : None,#
                          'd_sp'         : None,#Stator Shoe pole thickness
                          'r_si'         : None,#            
                          'alpha_ms'     : None, 
                          'd_ms'         : None,
                          'r_sh'         : None,
                          'r_so'         : None,
                          's_slot'       : None,
                          #'l_st'         : None,
                          'V_r'          : None,
                          #'d_sl'         : None,
                          #'delta_sl'     : None,
                          'n_m'          : None, # Number of magnet segments
                          }}
    
   
    required_materials={**RadialMachine.required_materials,
                        **{"rotor_mat":None,
                           "magnet_mat":None,
                           "air_mat":None}}
    required_winding={**RadialMachine.required_winding,
                        **{"n_phases":None,
                           "Key2":None}}
    required_nameplate={'mech_power'              : None, # kW
                        'mech_omega'              : None, # rad/s
                        'voltage_rating'          : None, # Vrms (line-to-line, Wye-Connect)
                        'Iq_rated_ratio'          : None, # per rated coil currents
                        }
    def __init__(self,machine_geometry_dict:dict,materials_dict:dict,
                 winding_dict:dict, nameplate_dict:dict,cls=None)->"BSPM_Machine_2D":
        """Initilize a BSPM_Machine object
        Keyword Argumets:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
        Return Values
            radial_machine: BSPM_Machine 
        """
        if cls==None:
            cls=BSPM_Machine_2D
        super().__init__(machine_geometry_dict, materials_dict, winding_dict, nameplate_dict,cls)
        

class BSPM_Machine_2D_Sleeved(BSPM_Machine_2D):
    """Bearingless Surface Mounted PM Machine Class subclass. 
    This is a sub class of the BSPM_Machine class"""
    
    required_geometry={**BSPM_Machine_2D.required_geometry,
                       **{'d_sl':None,
                          'delta_sl':None
                          }}
    
   
    required_materials={**BSPM_Machine_2D.required_materials,
                        **{'sleeve_mat':None}}
    
    required_winding={**BSPM_Machine_2D.required_winding}
                        
    required_nameplate={**BSPM_Machine_2D.required_nameplate}
    
    def __init__(self,machine_geometry_dict:dict,materials_dict:dict,
                 winding_dict:dict, nameplate_dict:dict,cls=None)->"BSPM_Machine_2D_Sleeved":
        """Initilize a BSPM_Machine object
        Keyword Argumets:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
            nameplate_dict: dict
        Return Values
            radial_machine: BSPM_Machine_2D_Sleeved
        """
        if cls==None:
            cls=BSPM_Machine_2D_Sleeved
        super().__init__(machine_geometry_dict, materials_dict, winding_dict, nameplate_dict,cls)
        
    