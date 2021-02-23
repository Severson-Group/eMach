# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 09:36:01 2021

@author: Martin Johnson
"""
from .machine import Machine,MachineComponent,MissingValueError,Winding

__all__ = ['BSPM_Machine']

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
    
# 