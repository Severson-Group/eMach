import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../../..")

from mach_eval.machines.bspm.bspm_settings import BSPM_EMAnalyzer_Settings


class BSPM_Settings_Handler:
    """This is a wrapper class designed to contain all relevant information
    on the operting point for obtaining eletrical performance evaluation of
    bearingless permanent magnet eletric machines
    """

    def __init__(self):
        pass

    def get_settings(self, x):
        try:
            em_op = BSPM_EMAnalyzer_Settings(
                Id=x[11],
                Iq=x[12],
                Ix=x[13],
                Iy=x[14],
                speed=x[15],
                ambient_temp=x[16],
                rotor_temp_rise=x[17],
            )
        except:
            em_op = BSPM_EMAnalyzer_Settings()
            print("WARNING: DEFAULT OPERATION POINTS USED")
        return em_op
