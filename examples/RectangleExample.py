# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 09:07:20 2021

@author: Martin Johnson
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
sys.path.append("..")
import desopt as do
import pygmo as pg
from typing import List,Tuple

class RectDesigner(do.Designer):
    """Class converts input tuple x into a Rectangle object"""
    
    def createDesign(self,x:tuple)->"Rectangle":
        """
        converts x tuple into a Rectangle object.

        Args:
            x (tuple): Input free variables.
            
        Returns:
            rect (Rectangle): Rectangle object
        """
        
        L=x[0]
        W=x[1]
        rect=Rectangle(L,W)
        return rect
    
class Rectangle(do.Design):
    """Class defines a rectangle object of Length and width
    
    Attributes:
        L (float): Length of Rectangle.
        W (float): Width of Rectangle.
    """
    
    def __init__(self,L:float,W:float):
        """Creates Rectangle object.

        Args:
            L (float): Length of Rectangle
            W (float): Width of Rectangle

        """
        self.L=L
        self.W=W

class RectEval(do.Evaluator):
    """"Class evaluates the rectangle object for area and perimeter"""
    
    def evaluate(self,rect):
        """Evalute area and perimeter of rectangle

        Args:
            rect (Rectangle): Rectangle Object

        Returns:
            [A,Per] (List[float,float]): Area and Perimeter of rectangle

        """
        A=rect.L*rect.W
        Per=2*rect.L+2*rect.W 
        return [A,Per]

class RectObj(do.Objective):
    """Class defines objectives of rectangle optimization"""

    def getObjectives(self,results:"List[float,float]"):
        """ Calculates objectives from evaluation results
        

        Args:
            results (List(float,float)): Results from RectEval

        Returns:
            Tuple[float,float]: Maximize Area, Minimize Perimeter
        """
        return (-results[0],results[1])
    
class DataHandler:
    def save(self,design,fullResults,objs):
        """Unimplented data handler"""
        pass
    

         
if __name__ == '__main__':
    des=RectDesigner()
    evaluator=RectEval()
    objectives=RectObj()
    dh=DataHandler()
    bounds=([0,0],[1,1])
    n_obj=2
    machDesProb=do.DesignProblem(des,evaluator,objectives,dh,
                                        bounds,n_obj)
    opt=do.DesignOptimizationMOEAD(machDesProb)
    pop=opt.run_optimization(500,10)
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits) 
    fig1=plt.figure()   
    plot1=plt.axes()
    fig1.add_axes(plot1)
    plot1.plot(fits[ndf[0],0],fits[ndf[0],1],'x')
    plot1.set_xlabel('Area')
    plot1.set_ylabel('Peremiter')
    plot1.set_title('Pareto Front')
    
    fig2=plt.figure()   
    plot2=plt.axes()
    fig2.add_axes(plot2)
    plot2.plot(vectors[ndf[0],0],vectors[ndf[0],1],'x')
    plot2.set_xlabel('L')
    plot2.set_ylabel('W')
    plot2.set_title('Vectors')
    