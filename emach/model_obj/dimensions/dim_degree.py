from .dim_angular import DimAngular

__all__ = ['DimDegree']


class DimDegree(DimAngular):
    def __new__(cls, value):
        if isinstance(value, DimAngular):
            tmp = DimDegree(value._to_dimensionless())
            return DimAngular.__new__(cls, DimDegree._from_dimensionless(tmp))
        else:
            return DimAngular.__new__(cls, value)

    @property
    def conversion_factor(self):
        return 0.017453293
