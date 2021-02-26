from .dim_linear import DimLinear

__all__ = ['DimMillimeter']

class DimMillimeter(DimLinear):
    def __new__(cls, value):
        return DimLinear.__new__(cls, value)

    @property
    def conversion_factor(self):
        return 1