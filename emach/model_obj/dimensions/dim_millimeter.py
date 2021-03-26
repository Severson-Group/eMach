from .dim_linear import DimLinear

__all__ = ['DimMillimeter']


class DimMillimeter(DimLinear):
    _conversion_factor = 1

    def __new__(cls, value):
        if isinstance(value, DimLinear):
            result = value._to_dimensionless()
            return DimLinear.__new__(cls, DimMillimeter._from_dimensionless(cls, result))
        else:
            return DimLinear.__new__(cls, value)
