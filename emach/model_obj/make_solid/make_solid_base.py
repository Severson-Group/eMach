from abc import ABC, abstractmethod

from ..location_3d import Location3D

class MakeSolidBase(ABC):
    
    def _create_attr(self, dictionary):
        for name, value in dictionary.items():
            setattr(self,'_'+name, value)
            
    @abstractmethod
    def _validate_attr(self):
        if not isinstance(self._location, Location3D):
            raise TypeError ("Expected input to be one of the following type: \
                             Location3D. Instead it was of type " + \
                             str(type(self._location)))  
            
    
    @property
    def location(self):
        return self._location
            
    @abstractmethod 
    def run(self, name, material, cs_token, maker):
        pass
    