from .bspm_settings import BSPM_EMAnalyzer_Settings


class BSPMSettingsHandler:
    """ This is a wrapper class designed to contain all relevant information on the operating point for obtaining
    electrical performance evaluation of bearingless permanent magnet electric machines
    """

    def __init__(self):
        pass

    def get_settings(self, x):
        em_op = BSPM_EMAnalyzer_Settings(Id=x[-7], Iq=x[-6], Ix=x[-5], Iy=x[-4], speed=x[-3], ambient_temp=x[-2],
                                         rotor_temp_rise=x[-1])
        return em_op
