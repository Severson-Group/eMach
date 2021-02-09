# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:07:14 2021

@author: Martin Johnson
"""

import pygmo as pg
from matplotlib import pyplot as plt

class MachineOptimization:
    def __init__(self,machine_design_problem):
        self.machine_design_problem=machine_design_problem

        
    def run_optimization(self, pop_size, gen_size):
        #######################################################################
        #############                   Create prob object                 ####
        #######################################################################
        
        
        prob = pg.problem(self.machine_design_problem)
        
        #######################################################################
        #############                   Create pop object                 #####
        #######################################################################
        
        
        pop = pg.population(prob,size=pop_size)
        # initial_pop=udp.initial_population(popsize)
        # for ind, chrom in enumerate(initial_pop):
        #     pop.push_back(chrom)
        
        #######################################################################
        #############                   Create algo object                #####
        #######################################################################
        
        algo = pg.algorithm(pg.moead(gen=gen_size, weight_generation="grid",
                                     decomposition="tchebycheff", 
                                     neighbours=20, 
                                     CR=1, F=0.5, eta_m=20, 
                                     realb=0.9, 
                                     limit=2, preserve_diversity=True))
        #######################################################################
        #############                   Run Optimization                  #####
        #######################################################################
        
        pop = algo.evolve(pop)
        
        return pop
        
        
       
