from abc import ABC, abstractmethod
from typing import List
from copy import deepcopy

from ..location_2d import Location2D


class CrossSectBase(ABC):
    """ Abstract base class for cross-sections"""

    def _create_attr(self, dictionary):
        for name, value in dictionary.items():
            setattr(self, '_' + name, value)

    @abstractmethod
    def _validate_attr(self):
        if isinstance(self._name, str):
            pass
        else:
            raise TypeError("cross_sect name not of type str")

        if isinstance(self._location, Location2D):
            pass
        else:
            raise TypeError("cross_sect location not of type Location2D")

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location

    @abstractmethod
    def draw(self, drawer: 'DrawerBase') -> 'CrossSectToken':
        """Draw cross-section with eMach tool

        Args:
            drawer : Drawer tool supported in eMach having draw_line anddraw_arc methods

        Returns:
            cs_token : Wrapper object holding information of inner coordinate of cross-section and tokens representing
                the lines and arcs that make up a cross-section
        """
        pass

    def clone(self, name: str, **kwargs: any):
        """Create clone of an already existing cross-section

        Args:
            name: Name that the cloned cross-section takes
            kwargs: List of arguments describing how cloned cross-section is different from the original
        Returns:
            cln: Object of type CrossSectBase representing the cloned cross-section
        """
        if self._name == name:
            raise AttributeError("name of clone same as name of original")

        cln = deepcopy(self)
        cln._name = name
        cln._create_attr(kwargs)

        return cln


class CrossSectToken:
    """Wrapper class to hold data generated upon creating a cross-section"""

    def __init__(self, inner_coord: List['DimLinear'], token: List['TokenDraw']):
        self.__inner_coord = inner_coord  # [x,y] coordinate of a point within the cross-section
        self.__token = token

    @property
    def inner_coord(self):
        return self.__inner_coord

    @property
    def token(self):
        return self.__token
