from .make_solid_base import MakeSolidBase
from ...tools.token_make import TokenMake
from ..dimensions.dim_linear import DimLinear

__all__ = ['MakeExtrude']

class MakeExtrude(MakeSolidBase):
    
    def __init__(self, **kwargs: any) -> None:
        self._create_attr(kwargs)
        
        super()._validate_attr()
        self._validate_attr()
        
    def _validate_attr(self):
        if isinstance(self._dim_depth, DimLinear):
            pass
        else:
            raise TypeError ("component depth not of type DimLinear")  
    
    
    def run(self, name, material, cs_token, maker):
        
        token1 = []
        for i in range(len(cs_token)):
            token1.append(maker.prepare_section(cs_token[i]))
        
        token2 = maker.extrude(name, material, self._dim_depth, token1)
        
        token_make = TokenMake(cs_token, token1, token2);
        return token_make
        