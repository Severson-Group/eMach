
from abc import ABC, abstractmethod
from typing import List
from copy import deepcopy

from ..location_2d import Location2D

class CrossSectBase(ABC):
    
    def _create_attr(self, dictionary):
        for name, value in dictionary.items():
            setattr(self,'_'+name, value)
    
    @abstractmethod
    def _validate_attr(self):
        
        if isinstance(self._name, str):
            pass
        else:
            raise TypeError ("cross_sect name not of type str")
            
        if isinstance(self._location, Location2D):
            pass
        else:
            raise TypeError ("cross_sect location not of type Location2D")
    
    @property
    def name(self):
        return self._name
    
    @property
    def location(self):
        return self._location
    
    @abstractmethod
    def draw(self, drawer: any) -> 'CrossSectToken': 
        '''
        Function to draw cross-sections using any drawer supported by eMach

        Parameters
        ----------
        drawer : any
            DESCRIPTION. Drawer tool supported in eMach having draw_line and 
            draw_arc methods

        Returns
        -------
        cs_token : CrossSectToken
            DESCRIPTION. Wrapper object holding information of inner coordinate
            of cross-section and tokens representing the cross-section

        '''
        pass
    
    def clone(self, name: str, **kwargs: any):
        '''
        Function to make a clone of an already exisitng cross-section. This 
        function sets the new cross-section to have a different name and location
        as compared to the original
        Parameters
        ----------
        name : str
        kwargs : any
        Returns
        -------
        cln : any
            DESCRIPTION. new cloned object
        '''
        if(self._name == name):
            raise AttributeError("name of clone same as name of original")
            
        cln = deepcopy(self)
        cln._name = name
        cln._create_attr(kwargs)
        
        return cln
    
class CrossSectToken():
    
    def __init__(self, inner_coord: List['DimLinear'], token: List['TokenDraw']):
        self.__inner_coord = inner_coord
        self.__token = token
        
    @property
    def inner_coord(self):
        return self.__inner_coord
    
    @property
    def token(self):
        return self.__token