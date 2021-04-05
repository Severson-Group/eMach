
__all__ = ['Component']

class Component():
    '''
    A logical group of cross sections that make up a component
    '''
    
    def __init__(self, name, cross_sections, material, make_solid):
        self._name = name
        self._cross_sections = cross_sections
        self._material = material
        self._make_solid = make_solid
    
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
        