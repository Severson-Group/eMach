
from.specification import Specification

class IMMachineSpec(Specification):
    '''
    This class is a wrapper for all information required by IM_Machine Architects
    '''
    
    def __init__(self,design_spec, rotor_core, stator_core , magnet , \
                 conductor, shaft, air = None, sleeve = None, hub = None):
        self.design_spec = design_spec
        self.rotor_material = rotor_core
        self.stator_material = stator_core
        self.magnet_material = magnet
        self.sleeve_material = sleeve
        self.coil_material = conductor
        self.shaft_material = shaft
        self.rotor_hub = hub
        self.air = air


    

    
    