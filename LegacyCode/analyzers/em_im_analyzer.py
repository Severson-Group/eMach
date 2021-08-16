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


    


