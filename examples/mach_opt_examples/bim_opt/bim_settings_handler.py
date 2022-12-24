import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../../..")

from mach_eval.machines.bim.bim_oper_pt import BIM_Machine_Oper_Pt


class BIM_Settings_Handler:
    """This is a wrapper class designed to contain all relevant information
    on the operting point for obtaining eletrical performance evaluation of
    bearingless induction machines
    """

    def __init__(self):
        pass

    def get_settings(self, x):
        em_op = BIM_Machine_Oper_Pt(
            speed=150000,
            slip_freq=1,
            It_ratio=0.975,
            Is_ratio=0.025,
            phi_t_0=0,
            phi_s_0=0,
            ambient_temp=75
            )
        # try:
        #     # em_op = BIM_Machine_Oper_Pt(
        #     #     speed=x[9],
        #     #     slip_freq=x[10],
        #     #     It_hat=x[11],
        #     #     Is_hat=x[12],
        #     #     phi_t_0=x[13],
        #     #     phi_s_0=x[14],
        #     #     ambient_temp=x[15],
        #     #     rotor_temp_rise=x[16],
        #     # )
        # except:
        #     em_op = BIM_Machine_Oper_Pt()
        #     print("WARNING: DEFAULT OPERATION POINTS USED")
        return em_op
