from time import time as clock_time
import os
import numpy as np
import pandas as pd

from .electrical_analysis import CrossSectInnerNotchedRotor as CrossSectInnerNotchedRotor
from .electrical_analysis import CrossSectStator as CrossSectStator
from .electrical_analysis.Location2D import Location2D

EPS = 1e-2 # unit: mm

class IM_EM_Analysis():

    def __init__(self, configuration):
        self.configuration = configuration
    
    def analyze(self, problem, counter = 0):

        self.machine_variant = problem.machine
        self.operating_point = problem.operating_point

        ####################################################
        # 01 Setting project name and output folder
        ####################################################
        self.project_name = 'proj_%d_' % (counter)

        expected_project_file = self.configuration['run_folder'] + "%s.jproj" % (self.project_name)

        # Create output folder
        if not os.path.isdir(self.configuration['JMAG_csv_folder']):
            os.makedirs(self.configuration['JMAG_csv_folder'])

            


    


