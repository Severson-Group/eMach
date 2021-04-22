# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 12:17:34 2021

@author: Martin Johnson
"""

import numpy as np
from matplotlib import pyplot as plt
import sys
sys.path.append("..")
import mach_opt as mo
import pygmo as pg
from typing import List,Tuple

class CubiodDesigner(mo.Designer):
    """Class converts input tuple x into a Cubiod object"""
    
    def createDesign(self,x:tuple)->"Cubiod":
        """
        converts x tuple into a Cubiod object.

        Args:
            x (tuple): Input free variables.
            
        Returns:
            cubiod (Cubiod): Cubiod object
        """
        
        L=x[0]
        W=x[1]
        H=x[2]
        cubiod=Cubiod(L,W,H)
        return cubiod
    
class Cubiod(mo.Design):
    """Class defines a cubiod object of Length and width
    
    Attributes:
        L (float): Length of Cubiod.
        W (float): Width of Cubiod.
        H (float); Height of Cubiod
    """
    
    def __init__(self,L:float,W:float,H:float):
        """Creates Cubiod object.

        Args:
            L (float): Length of Cubiod
            W (float): Width of Cubiod

        """
        self.L=L
        self.W=W
        self.H=H

class CubiodEval(mo.Evaluator):
    """"Class evaluates the cubiod object for volume and Surface Areas"""
    
    def evaluate(self,cubiod):
        """Evalute area and perimeter of cubiod

        Args:
            cubiod (Cubiod): Cubiod Object

        Returns:
            [V,SA,total,SA_Lateral] (List[float,float]): 
                Area and Perimeter of cubiodangle

        """
        V=cubiod.L*cubiod.W*cubiod.H
        SA_total=2*cubiod.L*cubiod.W+2*cubiod.W*cubiod.H+2*cubiod.L*cubiod.H
        SA_Lateral=2*cubiod.W*cubiod.H+2*cubiod.L*cubiod.H
        return [V,SA_total,SA_Lateral]

class CubiodObj(mo.Objective):
    """Class defines objectives of cubiod optimization"""

    def getObjectives(self,results:"List[float,float]"):
        """ Calculates objectives from evaluation results
        

        Args:
            results (List(float,float)): Results from CubiodEval

        Returns:
            Tuple[float,float]: Minimize volume, Maximize Total Surface Area,
                                Minimize Lateral Surface area
        """
        return (results[0],-results[1],results[2])
    
class DataHandler:
    def save(self,design,fullResults,objs):
        """Unimplented data handler"""
        pass
    
         
if __name__ == '__main__':
    des=CubiodDesigner()
    evaluator=CubiodEval()
    objectives=CubiodObj()
    dh=DataHandler()
    bounds=([.5,.1,.25],[10,3,5])
    n_obj=3
    machDesProb=mo.MachineDesignProblem(des,evaluator,objectives,dh,
                                        bounds,n_obj)
    opt=mo.MachineOptimizationMOEAD(machDesProb)
    pop=opt.run_optimization(496,10)
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits) 
   
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    im1=ax1.scatter(fits[ndf[0],0],fits[ndf[0],1],c=fits[ndf[0],2],marker='x')
    ax1.set_xlabel('Volume')
    ax1.set_ylabel('Total Surface Area')
    ax1.set_title('Pareto Front')
    cb1=fig1.colorbar(im1, ax=ax1,)
    cb1.set_label('Lateral Surface Area')

    fig2 = plt.figure()
    ax2 = fig2.add_subplot()
    im2=ax2.scatter(fits[ndf[0],1],fits[ndf[0],2],c=fits[ndf[0],0],marker='x')
    ax2.set_xlabel('Total Surface Area')
    ax2.set_ylabel('Lateral Surface Area')
    ax2.set_title('Pareto Front')
    cb2=fig2.colorbar(im2, ax=ax2,)
    cb2.set_label('Volume')
    
    fig3 = plt.figure()
    ax3 = fig3.add_subplot()
    im3=ax3.scatter(fits[ndf[0],2],fits[ndf[0],0],c=fits[ndf[0],1],marker='x')
    ax3.set_xlabel('Lateral Surface Area')
    ax3.set_ylabel('Volume')
    ax3.set_title('Pareto Front')
    cb3=fig3.colorbar(im3, ax=ax3,)
    cb3.set_label('Total Surface Area')
    