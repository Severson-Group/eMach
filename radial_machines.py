# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 09:36:01 2021

@author: Martin Johnson
"""
from machine import Machine,MachineComponent,MissingValueError,Winding

    
class Shaft(MachineComponent):

    def required_geometry():
        return ('r_sh',)
    def required_materials():
        return ('shaft_mat',)
    
    @property
    def r_sh(self):
        return self._machine_geometry_dict['r_sh']
    
    @property
    def shaft_mat(self):
        return self._materials_dict['shaft_mat']
    
class Rotor_Iron(MachineComponent):
    
    def required_geometry():
        return ('d_ri',)
    def required_materials():
        return ('rotor_iron_mat',)
    
    @property
    def d_ri(self):
        return self._machine_geometry_dict['d_ri']
    
    @property
    def rotor_iron_mat(self):
        return self._materials_dict['rotor_iron_mat']
    
class PM(MachineComponent):

    def required_geometry():
        return ('d_m','alpha_ms','alpha_m','n_m')
    def required_materials():
        return ('magnet_mat',)
    
    @property
    def d_m(self):
        return self._machine_geometry_dict['d_m']
    
    @property
    def alpha_m(self):
        return self._machine_geometry_dict['alpha_m']
    
    @property
    def alpha_ms(self):
        return self._machine_geometry_dict['alpha_ms']
    
    @property
    def n_m(self):
        return self._machine_geometry_dict['n_m']

    @property
    def magnet_mat(self):
        return self._materials_dict['magnet_mat']
        
class RotorSleeve(MachineComponent):
    def required_geometry():
        return ('d_sl',)
    def required_materials():
        return ('rotor_sleeve_mat',)
    
    @property
    def d_sl(self):
        return self._machine_geometry_dict['d_sl']
    
    @property
    def rotor_sleeve_mat(self):
        return self._materials_dict['rotor_sleeve_mat']
     
class PM_Rotor(Shaft,Rotor_Iron,PM,MachineComponent):

    
    def required_geometry():
        req_geo=('r_ro','d_mp','d_ms','p','V_r')
        for cl in PM_Rotor.__bases__:
            if cl.required_geometry() is not None:
                req_geo=req_geo+cl.required_geometry()
        return req_geo
    
    def required_materials():
        req_mat=tuple()
        for cl in PM_Rotor.__bases__:
            if cl.required_materials() is not None:
                req_mat=req_mat+cl.required_materials()
        return req_mat
    
    @property
    def d_mp(self):
        return self._machine_geometry_dict['d_mp']
    
    @property
    def d_ms(self):
        return self._machine_geometry_dict['d_ms']
    
    @property
    def r_ro(self):
        return self._machine_geometry_dict['r_ro']
    
    @property
    def p(self):
        return self._machine_geometry_dict['p']
    
    @property
    def V_r(self):
        return self._machine_geometry_dict['V_r']
       
class PM_Rotor_Sleeved(PM_Rotor,RotorSleeve,MachineComponent):

    
    def required_geometry():
        req_geo=('delta_sl',)
        for cl in PM_Rotor_Sleeved.__bases__:
            if cl.required_geometry() is not None:
                req_geo=req_geo+cl.required_geometry()
        return req_geo
    
    def required_materials():
        req_mat=tuple()
        for cl in PM_Rotor_Sleeved.__bases__:
            if cl.required_materials() is not None:
                req_mat=req_mat+cl.required_materials()
        return req_mat
    
    @property
    def delta_sl(self):
        return self._machine_geometry_dict['delta_sl']
    
class Stator(MachineComponent):
    
    def required_geometry():
        return ('alpha_st'    ,#Stator Tooth Angle
                'd_so'        ,#Stator 
                'w_st'        ,#Stator Tooth Width
                'd_st'        ,#Stator Tooth Length
                'd_sy'        ,#Stator Yoke width
                'alpha_so'    ,#
                'd_sp'        ,#Stator Shoe pole thickness
                'r_si'        ,#Stator Tooth Radius          
                'r_so'        ,
                's_slot'      ,
                'Q'
                #'l_st'        , #ADD to MOTOR
                )
    def required_materials():
        return ('stator_iron_mat',)
    
    @property
    def alpha_st(self):
        return self._machine_geometry_dict['alpha_st']
    
    @property
    def d_so(self):
        return self._machine_geometry_dict['d_so']

    @property
    def w_st(self):
        return self._machine_geometry_dict['w_st']
    
    @property
    def d_st(self):
        return self._machine_geometry_dict['d_st']
   
    @property
    def d_sy(self):
        return self._machine_geometry_dict['d_sy']
    
    @property
    def alpha_so(self):
        return self._machine_geometry_dict['alpha_so']

    @property
    def d_sp(self):
        return self._machine_geometry_dict['d_sp']
    
    @property
    def r_si(self):
        return self._machine_geometry_dict['r_si']
    
    @property
    def r_so(self):
        return self._machine_geometry_dict['r_so']
    
    @property
    def s_slot(self):
        return self._machine_geometry_dict['s_slot']
    
    @property
    def Q(self):
        return self._machine_geometry_dict['Q']
    
class BSPM_Winding(Winding):
    def required_geometry():
        return ()
    def required_materials():
        return ('coil_mat',)
    def required_winding():
        return ('Z_q',)
    
    @property
    def Z_q(self):
        return self._winding_dict['Z_q']
    
    @property
    def coil_mat(self):
        return self._materials_dict['coil_mat']
    
class BSPM_Machine(Machine,PM_Rotor_Sleeved,Stator,BSPM_Winding):
    
    def __init__(self,machine_geometry_dict:dict,materials_dict:dict,
                 winding_dict:dict,nameplate_dict:dict)->"BSPM_Machine":
        """ Creates a BSPM_Machine object
        Keyword Argumets:
            machine_geometry_dict: dict
            materials_dict: dict
            winding_dict: dict
        Return Values
            machine: BSPM_Machine 
        """
        cls=BSPM_Machine
        
        #first checks to see if the input dictionarys have the required values
        if cls.check_required_values(cls,machine_geometry_dict,
                                              materials_dict,
                                              winding_dict,
                                              nameplate_dict)== True:
            setattr(self, '_machine_geometry_dict',machine_geometry_dict)
            setattr(self, '_materials_dict',materials_dict) 
            setattr(self, '_winding_dict',winding_dict) 
            setattr(self, '_nameplate_dict',nameplate_dict) 

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
        for a in [[cls.required_geometry(),machine_geometry_dict],
                  [cls.required_materials(),materials_dict],
                  [cls.required_winding(),winding_dict],
                  [cls.required_nameplate(),nameplate_dict]]:
            for value in a[0] :
                if value in a[1]:
                    pass
                else:
                    missing_values.append(value)
        return missing_values
    

    def check_required_values(cls,machine_geometry_dict:dict,
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
        
    def required_geometry():
        req_geo=('delta_e','delta','l_st')
        for cl in BSPM_Machine.__bases__:
            if issubclass(cl,MachineComponent):
                if cl.required_geometry() is not None:
                    req_geo=req_geo+cl.required_geometry()
        return req_geo
    
    def required_materials():
        req_mat=('air_mat',)
        for cl in BSPM_Machine.__bases__:
            if issubclass(cl,MachineComponent):
                if cl.required_materials() is not None:
                    req_mat=req_mat+cl.required_materials()
        return req_mat
    
    def required_winding():
        req_wind=tuple()
        for cl in BSPM_Machine.__bases__:
            if issubclass(cl,Winding):
                if cl.required_winding() is not None:
                    req_wind=req_wind+cl.required_winding()
        return req_wind
    
    def required_nameplate():
        return ('mech_power'    , # kW
                'mech_omega'    , # rad/s
                'voltage_rating', # Vrms (line-to-line, Wye-Connect)
                'Iq_rated_ratio', # per rated coil currents
                )
    
    @property 
    def delta_e(self):
        return self._machine_geometry_dict['delta_e']
    
    @property 
    def delta(self):
        return self._machine_geometry_dict['delta']
    
    @property 
    def l_st(self):
        return self._machine_geometry_dict['l_st']
    
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
