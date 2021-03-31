from .make_solid_base import MakeSolidBase

__all__ = ['MakeExtrude']

class MakeExtrude(MakeSolidBase):
    
    def __init__(self, dim_depth):
        self._dim_depth = dim_depth
    
    def run(self, name, material, cs_token, maker):
        
        for i in range(len(cs_token)):
            token1 = maker.prepare_section(cs_token[i])
        
        token2 = maker.extrude(name, material, self._dim_depth)
        
        return token2
        