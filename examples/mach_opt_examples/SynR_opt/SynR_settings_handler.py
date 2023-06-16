import os
import sys

from mach_eval.machines.SynR.AM_SynR_machine_oper_pt import AM_SynR_Machine_Oper_Pt


class AM_SynR_Settings_Handler:
    """This is a wrapper class designed to contain all relevant information
    on the operting point for obtaining eletrical performance evaluation of
    additively manufactured synchronous reluctance machines
    """

    def __init__(self):
        pass

    def get_settings(self, x):
        em_op = AM_SynR_Machine_Oper_Pt(
            speed=70000,
            current_ratio=1,
            phi_0=0,
            ambient_temp=25,
            rotor_temp_rise=0,
            )

        return em_op