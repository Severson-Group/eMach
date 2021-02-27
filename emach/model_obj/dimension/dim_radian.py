from .dim_angular import DimAngular

__all__ = ['DimRadian']

class DimRadian(DimAngular):
    def __new__(cls, value):
        return DimAngular.__new__(cls, value)

    @property
    def conversion_factor(self):
        return 1
