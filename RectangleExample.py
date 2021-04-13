# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 09:07:20 2021

@author: Martin Johnson
"""
import numpy as np
from matplotlib import pyplot as plt
from MechEval import MachineOptimization
import pygmo as pg

class RectDesigner:
    def __init__(self):
        pass
    def createDesign(self,x):
        L=x[0]
        W=x[1]
        rect=Rectangle(L,W)
        return rect
    
class Rectangle:
    def __init__(self,L,W):
        self.L=L
        self.W=W

class RectEval:
    def __init__(self):
        pass
    def evaluate(self,rect):
        A=rect.L*rect.W
        Per=2*rect.L+2*rect.W 
        return [A,Per]

class RectObj:
    def __init__(self):
        pass
    def getObjectives(self,results):
        return (-results[0],results[1])
    
class DataHandler:
    def __init__(self):
        pass
    def save(self,design,fullResults,objs):
        pass
    
class MachineDesignProblem:
    def __init__(self,designer,evaluator,objectives,dh,bounds,n_obj):
        self.designer=designer
        self.evaluator=evaluator
        self.objectives=objectives
        self.dh=dh
        self.bounds=bounds
        self.n_obj=n_obj
    def fitness(self,x:'tuple')->'tuple':
        design=self.designer.createDesign(x)
        fullResults=self.evaluator.evaluate(design)
        objs=self.objectives.getObjectives(fullResults)
        self.dh.save(design,fullResults,objs)
        return objs
    def get_bounds(self):
        """Returns bounds for optimization problem""" 
        return self.bounds
    def get_nobj(self):
        """Returns number of objectievs of optimization problem"""
        return self.n_obj 
         
if __name__ == '__main__':
    des=RectDesigner()
    evaluator=RectEval()
    objectives=RectObj()
    dh=DataHandler()
    bounds=([0,0],[1,1])
    n_obj=2
    machDesProb=MachineDesignProblem(des,evaluator,objectives,dh,
                                        bounds,n_obj)
    opt=MachineOptimization(machDesProb)
    pop=opt.run_optimization(500,10)
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits) 
    fig2=plt.figure()   
    plot2=plt.axes()
    fig2.add_axes(plot2)
    plot2.plot(fits[ndf[0],0],fits[ndf[0],1],'x')
    plot2.set_xlabel('Area')
    plot2.set_ylabel('Peremiter')
    plot2.set_title('Pareto Front')
    
    fig3=plt.figure()   
    plot3=plt.axes()
    fig3.add_axes(plot3)
    plot3.plot(vectors[ndf[0],0],vectors[ndf[0],1],'x')
    plot3.set_xlabel('L')
    plot3.set_ylabel('W')
    plot3.set_title('Vectors')
    
    