from .dim_angular import DimAngular

__all__ = ['DimDegree']


class DimDegree(DimAngular):
    _conversion_factor = 0.017453293

    def __new__(cls, value):
        if isinstance(value, DimAngular):
            value = value._to_dimensionless()
            return DimAngular.__new__(cls, DimDegree._from_dimensionless(cls, value))
        else:
            return DimAngular.__new__(cls, value)
