# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 12:01:01 2022

@author: Martin Johnson
"""
import sys
from time import time as clock_time
import os
import numpy as np
import pandas as pd
import sys
sys.path.append("../..")
import electrical_analysis.JMAG as jm
from specifications.analyzer_config.em_fea_config import JMAG_FEA_Configuration

class JMAG_Gizmo(jm.JMAG):
    
    def __init__(self, configuration):
        super().__init__(configuration)
        self.counter = 0
        self.components =[None]
        self.materials = [None]
        self.conditions = [None]
    def set_up(self):
        print('Do application setup')
    def make_component(self,comp):
        if comp.material not in self.materials:
            self.add_material(comp.material)
        comp.make(self)
        self.components.append(comp)
    def add_material(self,material):
        self.materials.append(material)
        print('add ',material,' to tool')
    def add_motion_cond(self,target,param):
        if target in self.components:
            print('apply motion condition to: ',target.name)
            print(param)
    def add_current_cond(self,target,param):
        if target in self.components:
            print('apply current condition to: ',target.name)
            print(param)
    def add_force_cond(self,target,param):
        if target in self.components:
            print('apply motion condition to: ',target.name)
            print(param)
    def add_torque_cond(self,target,param):
        if target in self.components:
            print('apply motion condition to: ',target.name)
            print(param)
    def get_iron_loss(self,target):
        if target in self.components:
            print('get iron loss from condition to: ',target.name)
    def add_mesh(self,settings):
        print('Mesh study')
    def run_study(self):
        print('Run the FEA Study')
            
            
class DummyComponent:
    def __init__(self,name,material):
        self.name=name
        self.material=material
    def make(self,tool):
        print('Made ',self.name,' in tool')
class DummyMotionCond:
    def __init__(self,target,speed):
        self.target=target
        self.speed=speed
    def apply(self,tool,ind):
        tool.add_motion_cond(self.target,self.speed)
    def unapply(self,tool,ind):
        pass
class DummyForceCond:
    def __init__(self,target,force):
        self.target=target
        self.force=force
    def apply(self,tool,ind):
        tool.add_force_cond(self.target,self.force)
    def unapply(self,tool,ind):
        pass
class DummyCurrentCond:
    def __init__(self,target,amp):
        self.target=target
        self.amp=amp
    def apply(self,tool,ind):
        tool.add_current_cond(self.target,self.amp)
    def unapply(self,tool,ind):
        pass
class DummyTorqueCond:
    def __init__(self,target,Torque):
        self.target=target
        self.Torque=Torque
    def apply(self,tool):
        tool.add_torque_cond(self.target,self.torque)
    def unapply(self,tool,ind):
        pass
class DummyMeshSetting:
    def __init__(self,settings):
        self.settings=settings
    def apply(self,tool):
        tool.add_mesh(self.settings)
class DummyGetIronLoss:
    def __init__(self,target):
        self.target=target
        self.name='Iron Loss'
    def extract(self,tool):
        tool.get_iron_loss(self.target)
        

        

class FEA_Study:
    """FEA_Study is a class which holds all information about an study to be
    preformed in an FEA tool"""
    def __init__(self,eval_pts: int,
                 conditions,
                 settings,
                 get_results):
        self._eval_pts=eval_pts
        self._conditions=conditions
        self._cond_tokens=[]
        self._settings=settings
        self._setting_tokens=[]
        self._get_results=get_results
        self._res_tokens=[]

class FEA_ProblemDefinition():
    def __init__(self):
        pass
    def get_problem(self, state):
        pass

class FEA_Problem:
    """ FEA_Problem contains a set of components and studies to be preformed in 
    an FEA tool"""
    def __init__(self, components,
                 studies):
        self._components=components
        self._studies=studies
    
    @property
    def components(self):
        return self._components
    
    @property
    def studies(self):
        return self._studies
        
class FEA_Analyzer():
    """Analyzes FEA_Problems and returns the finished studies"""
    def __init__(self,tool):
        self._tool=tool
        self._tool.set_up()
    def analyze(self,problem: "FEA_Problem"):
             
        for comp in problem.components: 
            self._tool.make_component(comp)
            #Make each component in the FEA tool
            
        for study in problem.studies: 
            #Loop over each study
            results_dict=dict() 
            # Create a results dict to store data
            for get_res in study._get_results: 
                results_dict[get_res.name]=[None] * study._eval_pts 
                # add the result name to the dictionary and add a empty list of
                # the length of the number of eval points
            for setting in study._settings:
                setting.apply(self._tool)
                # apply the settings to the study 
            for ind in range(0,study._eval_pts):
                # for each eval pt in the study
                for cond in study._conditions:
                    cond.apply(self._tool,ind)
                    #Apply condition with its associated value at that point
                self._tool.run_study()
                # run the study for this eval pt
                for get_res in study._get_results:
                    results_dict[get_res.name][ind]=get_res.extract(self._tool)
                    #extract the requested result at this eval point and save
                for cond in study._conditions:
                    cond.unapply(self._tool,ind)
                    # unapply the condition to return to the inital state
            study.results=results_dict
            #store the results to the study
            
        return problem._studies
        #return the completed studies


rotor=DummyComponent('rotor','iron')
stator=DummyComponent('stator','iron')
coil=DummyComponent('coil','copper')
components=[rotor,stator,coil]

motionCond=DummyMotionCond(rotor,100)
currentCond=DummyCurrentCond(coil,10)
meshSett=DummyMeshSetting('Mesh Setting')
ironLoss=DummyGetIronLoss(stator)
conditions=[motionCond,currentCond]
settings=[meshSett,]
getRes=[ironLoss,]

study=FEA_Study(1,conditions,settings,getRes)
problem=FEA_Problem(components, [study,])
j_gizmo=JMAG_Gizmo(JMAG_FEA_Configuration)   
fea_ana=FEA_Analyzer(j_gizmo) 
fea_ana.analyze(problem)
