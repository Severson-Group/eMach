from .dim_linear import DimLinear

__all__ = ['DimMillimeter']


class DimMillimeter(DimLinear):
    def __new__(cls, value):
        if isinstance(value, DimLinear):
            tmp = DimMillimeter(value._to_dimensionless())
            return DimLinear.__new__(cls, DimMillimeter._from_dimensionless(tmp))
        else:
            return DimLinear.__new__(cls, value)

    @property
    def conversion_factor(self):
        return 1
