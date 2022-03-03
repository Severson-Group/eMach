# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 09:07:20 2021

@author: Martin Johnson
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
sys.path.append("..")
import des_opt as do
import pygmo as pg
from typing import List,Tuple

class RectDesigner(do.Designer):
    """Class converts input tuple x into a Rectangle object"""
    
    def create_design(self,x:tuple)->"Rectangle":
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

class RectDesignSpace(do.DesignSpace):
    """Class defines objectives of rectangle optimization"""

    def __init__(self,bounds,n_obj):
        self._n_obj=n_obj
        self._bounds=bounds
        
    def get_objectives(self, valid_constraints, full_results) -> tuple:
        """ Calculates objectives from evaluation results
        

        Args:
            results (List(float,float)): Results from RectEval

        Returns:
            Tuple[float,float]: Maximize Area, Minimize Perimeter
        """
        return (-full_results[0],full_results[1])
    
    def check_constraints(self, full_results) -> bool:
        return True
    
    @property
    def n_obj(self) -> int:
        return self._n_obj
    
    @property
    def bounds(self) -> tuple:
        return self._bounds
    
class DataHandler:
    def save_to_archive(self, x, design, full_results, objs):
        """Unimplented data handler"""
        pass
    def save_designer(self, designer):
        pass

         
if __name__ == '__main__':
    
    des=RectDesigner()
    evaluator=RectEval()
    dh=DataHandler()
    bounds=([0,0],[1,1])
    n_obj=2
    ds=RectDesignSpace(bounds,n_obj)
    machDesProb=do.DesignProblem(des,evaluator,ds,dh)
    
    opt=do.DesignOptimizationMOEAD(machDesProb)
    pop_size=50
    pop=opt.initial_pop(pop_size)
    gen_size=10    
    pop=opt.run_optimization(pop,gen_size)
    
    fig1=plt.figure()   
    plot1=plt.axes()
    fig1.add_axes(plot1)
    fits, vectors = pop.get_f(), pop.get_x()
    ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits) 
    plot1.plot(fits[ndf[0],0],fits[ndf[0],1],'x')
    plot1.set_xlabel('Area')
    plot1.set_ylabel('Peremiter')
    plot1.set_title('Pareto Front')
    plot1.savefig("test.svg")

    