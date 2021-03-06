from .dim_linear import DimLinear

__all__ = ['DimInch']

class DimInch(DimLinear):
    def __new__(cls, value):
        return DimLinear.__new__(cls, value)
    
    @property
    def conversion_factor(self):
        return 25.4
    


