from .make_solid.make_solid_base import MakeSolidBase
from .materials.material_generic import MaterialGeneric

__all__ = ['Component']

class Component():
    '''
    A logical group of cross sections that make up a component
    '''
    
    def __init__(self, **kwargs):
        self._create_attr(kwargs)
        self._validate_attr()
        
    @property
    def name(self):
        return self._name
    
    @property
    def cross_sections(self):
        return self._cross_sections
    
    @property
    def material(self):
        return self._material
    
    @property
    def make_solid(self):
        return self._make_solid
        
    def make(self, drawer, maker):
        cs = self.draw(drawer)
        token_make = self._make_solid.run(self._name, self._material._name, cs, maker)
        return token_make
    
    def draw(self, drawer):
        cs = []
        for i in range(len(self._cross_sections)):
            cs.append(self._cross_sections[i].draw(drawer))
        
        return cs
    
    def _create_attr(self, dictionary):
        for name, value in dictionary.items():
            setattr(self,'_'+name, value)
    
    def _validate_attr(self):
        
        if isinstance(self._name, str):
            pass
        else:
            raise TypeError ("Component name not of type str")
        
        if isinstance(self._make_solid, MakeSolidBase):
            pass
        else:
            raise TypeError ("Component make solid function not of type MakeSolidBase")
        
        if isinstance(self._material, MaterialGeneric):
            pass
        else:
            raise TypeError ("Component material not of type MaterialGeneric")
        