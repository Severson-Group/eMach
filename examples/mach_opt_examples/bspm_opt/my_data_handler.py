import os
import sys

# add the directory 3 levels above this file's directory to path for module import
sys.path.append(os.path.dirname(__file__)+"/../../..")

import mach_opt as mo

class MyDataHandler(mo.DataHandler):

    def select_designs(self):
        archive = self.load_from_archive()
        i = 0
        for data in archive:
            if data.full_results is None:
                continue
            final_state = data.full_results[-1][-1]
            Ea = final_state.conditions.em["Ea"]
            i = i+1
            if data.objs[0]<-8 and data.objs[1]<-97.7 and Ea<1 and data.objs[2]<2:
                print("Design is ", final_state.design.machine.name)
                print(data.objs, Ea)
        
    def get_design(self, name):
        archive = self.load_from_archive()
        i = 0
        for data in archive:
            if data.full_results is None:
                continue

            final_state = data.full_results[-1][-1]
            design = final_state.design
            machine = design.machine
            if machine.name == name:
                return design
        return None
                
