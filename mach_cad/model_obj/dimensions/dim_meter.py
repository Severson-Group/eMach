from .dim_linear import DimLinear

__all__ = ['DimMeter']


class DimMeter(DimLinear):
    _conversion_factor = 1000

    def __new__(cls, value):
        if isinstance(value, DimLinear):
            result = value._to_dimensionless()
            return DimLinear.__new__(cls, DimMeter._from_dimensionless(cls, result))
        else:
            return DimLinear.__new__(cls, value)
