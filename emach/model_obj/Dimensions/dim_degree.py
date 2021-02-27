from .dim_angular import DimAngular

__all__ = ['DimDegree']

class DimDegree(DimAngular):
    def __new__(cls, value):
        return DimAngular.__new__(cls, value)


    @property
    def conversion_factor(self):
        return 3.14159265359/180

