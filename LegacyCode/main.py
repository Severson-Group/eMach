# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 11:00:02 2021

@author: Martin Johnson
"""

import numpy as np
from matplotlib import pyplot as plt
import sys
from typing import List,Tuple,Any
from copy import deepcopy
import pygmo as pg

sys.path.append("..")
import desopt as do
import macheval as me

from MachineDesign.bspm_architect import BSPMArchitectType1 as Architect
from MachineDesign.bspm_settingshandler import BSPMSettingsHandler 

from MachineEvaluation.Structural import SleeveDesignStep
from MachineEvaluation.EM import EMStep
from MachineEvaluation.Misc import LengthScaleStep
from MachineEvaluation.Thermal import ThermalStep
from AnalyzerSettings import (SleeveDesignSettings,EMStepSettings,
                              LengthScaleStepSettings,ThermalStepSettings)

from Objectives.bspm_objective import BSPMObjective1 as Objective

from DataHandler import DataHandler


#Create Designer
settingsHandler=BSPMSettingsHandler() #TODO define settings
arch=Architect()
des=me.MachineDesigner(arch,settingsHandler)

#Create evaluation steps
sleeveDesignStep = SleeveDesignStep(SleeveDesignSettings)
emStep = EMStep(EMStepSettings)
lengthScaleStep = LengthScaleStep(LengthScaleStepSettings)
thermalStep = ThermalStep(ThermalStepSettings)
evalSteps=[sleeveDesignStep,emStep,lengthScaleStep,thermalStep]

#Create Evaluator
evaluator=me.MachineEvaluator(evalSteps)
objectives=Objective()
dh=DataHandler()#TODO Define Datahandler

#set evaluation bounds
bounds=([.1,10E3,.1E-3,10E-3,1000*2*np.pi/60],
        [1,100E3,10E-3,95.5E-3,15000*2*np.pi/60])#TODO Define bounds

#set number of objectives
n_obj=3 #TODO Define bounds

#Create Machine Design Problem
machDesProb=do.DesignProblem(des,evaluator,objectives,dh,
                                    bounds,n_obj)

#Run Optimization
opt=do.DesignOptimizationMOEAD(machDesProb)
pop=opt.run_optimization(496,500)
fits, vectors = pop.get_f(), pop.get_x()
ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits) 

fig1 = plt.figure()
ax1 = fig1.add_subplot()
im1=ax1.scatter(fits[ndf[0],0],fits[ndf[0],1],c=fits[ndf[0],2],marker='x')
ax1.set_xlabel('-Efficiency')
ax1.set_ylabel('Cost [$]')
ax1.set_title('Pareto Front')
cb1=fig1.colorbar(im1, ax=ax1,)
cb1.set_label('Torque Ripple [ ]')

fig2 = plt.figure()
ax2 = fig2.add_subplot()
im2=ax2.scatter(fits[ndf[0],1],fits[ndf[0],2],c=fits[ndf[0],0],marker='x')
ax2.set_xlabel('Cost [$]')
ax2.set_ylabel('Torque Ripple [ ]')
ax2.set_title('Pareto Front')
cb2=fig2.colorbar(im2, ax=ax2,)
cb2.set_label('-Efficiency')

fig3 = plt.figure()
ax3 = fig3.add_subplot()
im3=ax3.scatter(fits[ndf[0],2],fits[ndf[0],0],c=fits[ndf[0],1],marker='x')
ax3.set_xlabel('Torque Ripple [ ]')
ax3.set_ylabel('-Efficiency')
ax3.set_title('Pareto Front')
cb3=fig3.colorbar(im3, ax=ax3,)
cb3.set_label('Cost [$]')