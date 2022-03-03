from abc import ABC, abstractmethod

from ..location_3d import Location3D


class MakeSolidBase(ABC):
    def _create_attr(self, dictionary: dict):
        for name, value in dictionary.items():
            setattr(self, '_' + name, value)

    @property
    def location(self):
        return self._location

    @abstractmethod
    def _validate_attr(self):
        """Check Location3D attribute required in all Components"""
        if not isinstance(self._location, Location3D):
            raise TypeError("Expected input to be one of the following type: \
                             Location3D. Instead it was of type " + str(type(self._location)))

    @abstractmethod
    def run(self, name: str, material: str, cs_token: list('CrossSectToken'), maker: 'MakerBase'):
        """Use tool to create 3D component"""
        pass
