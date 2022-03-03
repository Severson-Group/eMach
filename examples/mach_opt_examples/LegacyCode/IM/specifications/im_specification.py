
from.specification import Specification

class IMMachineSpec(Specification):
    '''
    This class is a wrapper for all information required by IM_Machine Architects
    '''

    
    def __init__(self,design_spec, rotor_core, stator_core , rotor_bar , \
                 conductor, shaft, air = None, hub = None):
        self.design_spec = design_spec
        self.rotor_material = rotor_core
        self.stator_material = stator_core
        self.rotor_bar_material = rotor_bar
        self.coil_material = conductor
        self.shaft_material = shaft
        self.rotor_hub = hub
        self.air = air


    

    
    