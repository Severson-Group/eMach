from .dim_linear import DimLinear

__all__ = ['DimInch']


class DimInch(DimLinear):
    def __new__(cls, value):
        if isinstance(value, DimLinear):
            tmp = DimInch(value._to_dimensionless())
            return DimLinear.__new__(cls, DimInch._from_dimensionless(tmp))
        else:
            return DimLinear.__new__(cls, value)

    @property
    def conversion_factor(self):
        return 25.4
