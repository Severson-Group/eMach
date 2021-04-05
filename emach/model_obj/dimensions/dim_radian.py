from .dim_angular import DimAngular

__all__ = ['DimRadian']


class DimRadian(DimAngular):
    _conversion_factor = 1

    def __new__(cls, value):
        if isinstance(value, DimAngular):
            value = value._to_dimensionless()
            return DimAngular.__new__(cls, DimRadian._from_dimensionless(cls, value))
        else:
            return DimAngular.__new__(cls, value)
