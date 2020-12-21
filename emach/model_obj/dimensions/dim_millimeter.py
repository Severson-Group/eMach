from .dim_linear import DimLinear

__all__ = ['DimMillimeter']

class DimMillimeter(DimLinear):
    def __new__(cls, value):
        if type(value).__bases__[0] is DimLinear:
            value = value.to_mm()
        return DimLinear.__new__(cls, value)

    def to_mm(self):
        return self

    def to_inch(self):
        return self / 25.4

    def _to_dimesionless(self):

        return float(self)

    def _from_dimesionless(var):

        x = var
        return DimMillimeter(x)
