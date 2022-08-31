import pickle
import pygmo as pg
import os
import sys

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")

import mach_opt as mo

class MyDataHandler(mo.DataHandler):
    # def __init__(self, archive_filepath, designer_filepath):
    #     self.archive_filepath = archive_filepath
    #     self.designer_filepath = designer_filepath

    # def save_to_archive(self, x, design, full_results, objs):
    #     # assign relevant data to OptiData class attributes
    #     opti_data = mo.OptiData(x=x, design=design, full_results=full_results, objs=objs)
    #     # write to pkl file. 'ab' indicates binary append
    #     with open(self.archive_filepath, 'ab') as archive:
    #         pickle.dump(opti_data, archive, -1)

    # def load_from_archive(self):
    #     with open(self.archive_filepath, 'rb') as f:
    #         while 1:
    #             try:
    #                 yield pickle.load(f)  # use generator
    #             except EOFError:
    #                 break

    # def save_designer(self, designer):
    #     with open(self.designer_filepath, 'wb') as des:
    #         pickle.dump(designer, des, -1)
            
    # def get_archive_data(self):
    #     archive = self.load_from_archive()
    #     fitness = []
    #     free_vars = []
    #     for data in archive:
    #         fitness.append(data.objs)
    #         free_vars.append(data.x)
    #     return fitness, free_vars
    
    # def get_pareto_designs(self):
    #     archive = self.load_from_archive()
    #     fitness, free_vars = self.get_archive_data()
        
    #     ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fitness)
    #     fronts_index = ndf[0]
        
    #     i = 0
    #     for data in archive:
    #         if i in fronts_index:
    #             yield data
    #         i = i+1
    
    # def get_pareto_fitness_freevars(self):
    #     archive = self.get_pareto_designs()
    #     fitness = []
    #     free_vars = []
    #     rated_power = []
    #     for data in archive:
    #         fitness.append(data.objs)
    #         free_vars.append(data.x)
            
    #     return fitness, free_vars

    def select_designs(self):
        archive = self.load_from_archive()
        i = 0
        for data in archive:
            if data.full_results is None:
                continue
            final_state = data.full_results[-1][-1]
            Ea = final_state.conditions.em["Ea"]
            i = i+1
            if data.objs[1]<-97.7 and Ea<1 and data.objs[2]<2:
                print("Design is ", final_state.design.machine.name)
                print(data.objs, Ea)
        
    def get_machine(self, name):
        archive = self.load_from_archive()
        i = 0
        for data in archive:
            if data.full_results is None:
                continue

            final_state = data.full_results[-1][-1]
            machine = final_state.design.machine
            if machine.name == name:
                return machine
        return None
                
