from .dim_linear import DimLinear

__all__ = ['DimInch']


class DimInch(DimLinear):
    _conversion_factor = 25.4

    def __new__(cls, value):
        if isinstance(value, DimLinear):
            result = value._to_dimensionless()
            return DimLinear.__new__(cls, DimInch._from_dimensionless(cls, result))
        else:
            return DimLinear.__new__(cls, value)
