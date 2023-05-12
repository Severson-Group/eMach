import os
import sys

import mach_opt as mo

class MyDataHandler(mo.DataHandler):

    def select_designs(self):
        archive = self.load_from_archive()
        i = 0
        for data in archive:
            if data.full_results is None:
                continue
            final_state = data.full_results[-1][-1]
            i = i+1
            if data.objs[1]<-90.0 and data.objs[2]<0.3:
                print("Design is ", final_state.design.machine.name)
                print(data.objs)
        
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