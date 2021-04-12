from .make_solid_base import MakeSolidBase
from ...tools.token_make import TokenMake
from ..dimensions.dim_angular import DimAngular
from ..location_2d import Location2D

__all__ = ['MakeRevolve']

class MakeRevolve(MakeSolidBase):
    
    def __init__(self, **kwargs: any) -> None:
        self._create_attr(kwargs)
        
        super()._validate_attr()
        self._validate_attr()
        
    def _validate_attr(self):
        if isinstance(self._dim_angle, DimAngular):
            pass
        else:
            raise TypeError ("component angle not of type DimAngular")
            
        if isinstance(self._dim_center, Location2D):
            pass
        else:
            raise TypeError ("component angle not of type Location2D") 
            
        if isinstance(self._dim_axis, Location2D):
            pass
        else:
            raise TypeError ("component angle not of type Location2D")  
    
    
    def run(self, name, material, cs_token, maker):
        
        token1 = []
        for i in range(len(cs_token)):
            token1.append(maker.prepare_section(cs_token[i]))
        
        token2 = maker.revolve(name, material, self._dim_center, self._dim_axis, \
                               self._dim_angle, token1)
        
        token_make = TokenMake(cs_token, token1, token2);
        return token_make
        

