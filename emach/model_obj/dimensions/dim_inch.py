from .dim_linear import DimLinear

__all__ = ['DimInch']

class DimInch(DimLinear):
    def __new__(cls, value):
        if (isinstance(value, DimLinear)):
            return DimLinear.__new__(cls, value.conversion_factor)
        else:
            return DimLinear.__new__(cls, value)
    
    @property
    def conversion_factor(self):
        return 25.4
    


