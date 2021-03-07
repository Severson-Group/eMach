from .dim_angular import DimAngular

__all__ = ['DimRadian']


class DimRadian(DimAngular):
    def __new__(cls, value):
        if isinstance(value, DimAngular):
            tmp = DimRadian(value._to_dimensionless())
            return DimAngular.__new__(cls, DimRadian._from_dimensionless(tmp))
        else:
            return DimAngular.__new__(cls, value)

    @property
    def conversion_factor(self):
        return 1
