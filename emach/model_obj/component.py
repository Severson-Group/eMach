from copy import deepcopy

from .make_solid.make_solid_base import MakeSolidBase
from .materials.material_generic import MaterialGeneric
from .cross_sects.cross_sect_base import CrossSectBase

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
        token_make = self.make_solid.run(self.name, self.material.name, cs, maker)
        return token_make
    
    def draw(self, drawer):
        cs = []
        for i in range(len(self.cross_sections)):
            cs.append(self.cross_sections[i].draw(drawer))
        
        return cs
    
    def clone(self, name, **kwargs):
        if(self.name == name):
            raise AttributeError("name of clone same as name of original")
        cln = deepcopy(self)
        cln._name = name
        cln._create_attr(kwargs)
        return cln
    
    def _create_attr(self, dictionary):
        for name, value in dictionary.items():
            setattr(self,'_'+name, value)
    
    def _validate_attr(self):
        
        if not isinstance(self._name, str):
            raise TypeError ("Expected input to be one of the following type: \
                             str. Instead it was of type " + \
                             str(type(self._name)))
                
        if not isinstance(self._make_solid, MakeSolidBase):
            raise TypeError ("Expected input to be one of the following type: \
                             MakeSolidBase. Instead it was of type " + \
                             str(type(self._make_solid)))
                
        if not isinstance(self._material, MaterialGeneric):
            raise TypeError ("Expected input to be one of the following type: \
                             MaterialGeneric. Instead it was of type " + \
                             str(type(self._material)))
                
        for i in range(len(self._cross_sections)):
            if not isinstance(self._cross_sections[i],CrossSectBase):
                raise TypeError ("Expected input to be one of the following type: \
                             CrossSectBase. Instead it was of type " + \
                             str(type(self._cross_sections[i])))
        