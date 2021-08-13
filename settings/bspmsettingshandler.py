from .bspm_settings import BSPM_EMAnalyzer_Settings


class BSPMSettingsHandler():
    """ This is a wrapper class designed to contain all relevant information on the operating point for obtaining
    electrical performance evaluation of bearingless permanent magnet electric machines
    """

    def __init__(self):
        pass

    def get_settings(self, x):
        em_op = BSPM_EMAnalyzer_Settings(Id=0, Iq=0.95, Ix=0, Iy=0.05, speed=160000, ambient_temp=25,
                                         rotor_temp_rise=80)
        return em_op
