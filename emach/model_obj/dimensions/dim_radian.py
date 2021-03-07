from .dim_angular import DimAngular

__all__ = ['DimRadian']


class DimRadian(DimAngular):
    def __new__(cls, value):
        if isinstance(value, DimAngular):
            value.result = value._to_dimensionless()
            return DimAngular.__new__(cls, cls._from_dimensionless(value))
        else:
            return DimAngular.__new__(cls, value)

    @property
    def conversion_factor(self):
        return 1
