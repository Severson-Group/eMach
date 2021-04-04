from abc import abstractmethod, ABC


class DimBase(float, ABC):

    @abstractmethod
    def _conversion_factor(self):
        pass

    def __new__(cls, value):
        return float.__new__(cls, value)

    def __add__(self, other):
        add = self._to_dimensionless() + other._to_dimensionless()
        return type(self)._from_dimensionless(type(self), add)

    def __sub__(self, other):
        sub = self._to_dimensionless() - other._to_dimensionless()
        return type(self)._from_dimensionless(type(self), sub)

    def __mul__(self, other):
        if isinstance(self, DimBase) and isinstance(other, DimBase):
            raise Exception('Multiplication Not valid')

        if isinstance(self, DimBase):
            mul = other * (self._to_dimensionless())
            return type(self)._from_dimensionless(type(self), mul)

    def __rmul__(self, other):
        if isinstance(self, DimBase) and isinstance(other, DimBase):
            raise Exception('Multiplication Not valid')

        if isinstance(self, DimBase):
            mul = other * (self._to_dimensionless())
            type(self)._from_dimensionless(type(self), mul)

    def __truediv__(self, other):
        if isinstance(other, DimBase):
            div = self._to_dimensionless() / other._to_dimensionless()
            return div
        else:
            div = (self._to_dimensionless()) / (other)
            return type(self)._from_dimensionless(type(self), div)

    def __rtruediv__(self, other):
        raise Exception('Division not valid')

    def _to_dimensionless(self):
        return float(self) * self._conversion_factor

    def _from_dimensionless(cls, value):
        x = value / cls._conversion_factor
        return cls(x)

    def __neg__(self):
        return self * -1

    def __pos__(self):
        if self < 0:
            return self * -1
        else:
            return self

