from abc import ABC, abstractmethod

from ..location_3d import Location3D

class MakeSolidBase(ABC):
    
    def _create_attr(self, dictionary):
        for name, value in dictionary.items():
            setattr(self,'_'+name, value)
            
    @abstractmethod
    def _validate_attr(self):
        
        if isinstance(self._location, Location3D):
            pass
        else:
            raise TypeError ("Component location not of type Location3D")  
            
    @abstractmethod 
    def run(self, name, material, cs_token, maker):
        pass
    