from time import time as clock_time
import os
import femm
# import sys
# sys.path.append("..")
# import sys
# sys.path.append('FEMM_Solver.py')
import numpy as np
import pandas as pd

from .electrical_analysis import CrossSectInnerNotchedRotor as CrossSectInnerNotchedRotor
from .electrical_analysis import CrossSectStator as CrossSectStator
from .electrical_analysis.Location2D import Location2D

# from analyzers import FEMM_Solver
from .FEMM_Solver import FEMM_Solver
EPS = 1e-2 # unit: mm

class IM_EM_Analysis():

    def __init__(self, configuration):
        self.configuration = configuration

    def create_im_variant(self):
        # self.im =IM_EM_Analysis()
        self.im.Angle_RotorSlotSpan = 2


    def analyze(self, problem, counter = 0):

        self.machine_variant = problem.machine
        self.operating_point = problem.operating_point
        problem.configuration = self.configuration
        ####################################################
        # 01 Setting project name and output folder
        ####################################################
        self.project_name = 'proj_%d_' % (counter)

        expected_project_file = self.configuration['run_folder'] + "%s.jproj" % (self.project_name)

        # Create output folder
        if not os.path.isdir(self.configuration['JMAG_csv_folder']):
            os.makedirs(self.configuration['JMAG_csv_folder'])


        self.machine_variant.fea_config_dict = self.configuration
        self.machine_variant.bool_initial_design = self.configuration['bool_initial_design']
        self.machine_variant.ID = self.project_name
        self.bool_run_in_JMAG_Script_Editor = False

        self.femm_solver = FEMM_Solver(self.machine_variant, flag_read_from_jmag=False, freq=50)  # eddy+static

        self.femm_solver.greedy_search_for_breakdown_slip(self.configuration['JMAG_csv_folder'], self.project_name,
                                                          bool_run_in_JMAG_Script_Editor=self.bool_run_in_JMAG_Script_Editor,
                                                          fraction=1)  # 转子导条必须形成通路
        # self.femm_solver.run_rotating_static_FEA()






            


    


