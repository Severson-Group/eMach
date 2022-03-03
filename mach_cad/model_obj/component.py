from copy import deepcopy

from .make_solid.make_solid_base import MakeSolidBase
from .materials.material_generic import MaterialGeneric
from .cross_sects.cross_sect_base import CrossSectBase

__all__ = ['Component']


class Component:
    """A logical group of cross sections that make up a component"""


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

    def make(self, drawer: 'DrawerBase', maker: 'MakerBase'):
        """Draw and make a Component

        Function to draw and make a component in DrawerBase and MakerBase supported tools of choice. In most cases, both
        arguments will be the same.
        Args:
            drawer: Handle to tool used to draw 2D cross-section
            maker: Handle to tool used to make 3D components
        Returns:
            token_make: Object of type TokenMake holding return values/handles to cross-sections/components obtained
            from the tool upon performing the requested operations
        """
        cs = self.draw(drawer)
        token_make = self.make_solid.run(self.name, self.material.name, cs, maker)
        return token_make

    def draw(self, drawer: 'DrawerBase'):
        """Draw a cross-section in drawer tool

        Args:
            drawer: Handle to tool used to draw 2D cross-section
        Returns:
            cs: List of CrossSectToken objects holding information on inner coordinate and lines/arcs that make up a
            cross-section
        """
        cs = []
        for i in range(len(self.cross_sections)):
            cs.append(self.cross_sections[i].draw(drawer))
        return cs

    def clone(self, name: str, **kwargs):
        """Create clone of an already existing component

        Args:
            name: Name that the cloned component takes
            kwargs: List of arguments describing how cloned component is different from the original
        Returns:
            cln: Object of Component class representing cloned component
        """
        if self.name == name:
            raise AttributeError("A new name must be specified for the cloned object")
        cln = deepcopy(self)
        cln._name = name
        cln._create_attr(kwargs)
        return cln

    def _create_attr(self, dictionary: dict):
        for name, value in dictionary.items():
            setattr(self, '_' + name, value)

    def _validate_attr(self):

        if not isinstance(self._name, str):
            raise TypeError("Expected input to be one of the following type: \
                             str. Instead it was of type " + \
                            str(type(self._name)))

        if not isinstance(self._make_solid, MakeSolidBase):
            raise TypeError("Expected input to be one of the following type: \
                             MakeSolidBase. Instead it was of type " + \
                            str(type(self._make_solid)))

        if not isinstance(self._material, MaterialGeneric):
            raise TypeError("Expected input to be one of the following type: \
                             MaterialGeneric. Instead it was of type " + \
                            str(type(self._material)))

        for i in range(len(self._cross_sections)):
            if not isinstance(self._cross_sections[i], CrossSectBase):
                raise TypeError("Expected input to be one of the following type: \
                             CrossSectBase. Instead it was of type " + \
                                str(type(self._cross_sections[i])))
