from .dim_base import DimBase


class DimLinear(DimBase):
    def __new__(cls, value):
        return DimBase.__new__(cls, value)

    def __add__(self, other):
        add = self._to_dimensionless() + other._to_dimensionless()
        result = type(self)(add)
        return type(self)._from_dimensionless(result)

    def __sub__(self, other):
        sub = self._to_dimensionless() - other._to_dimensionless()
        result = type(self)(sub)
        return type(self)._from_dimensionless(result)

    def __mul__(self, other):
        if isinstance(self, DimLinear) and isinstance(other, DimLinear):
            raise Exception('Multiplication Not valid')

        if isinstance(self, DimLinear):
            mul = other * (self._to_dimensionless())
            result = type(self)(mul)
            return type(self)._from_dimensionless(result)

    def __rmul__(self, other):
        if isinstance(self, DimLinear) and isinstance(other, DimLinear):
            raise Exception('Multiplication Not valid')

        if isinstance(self, DimLinear):
            mul = other * (self._to_dimensionless())
            result = type(self)(mul)
            return type(self)._from_dimensionless(result)

    def __truediv__(self, other):
        if isinstance(other, DimLinear):
            div = self._to_dimensionless() / other._to_dimensionless()
            return div
        else:
            div = (self._to_dimensionless()) / (other)
            result = type(self)(div)
            return type(self)._from_dimensionless(result)

    def __rtruediv__(self, other):
        raise Exception('Division not valid')
