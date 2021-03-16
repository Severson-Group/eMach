
from abc import abstractmethod, ABC


class DimBase(float, ABC):
    def __new__(cls, value):
        return float.__new__(cls, value)
    def __init__(self,data):
        self.data = float(data)


    def __add__(self, other):
        add = self._to_dimensionless() + other._to_dimensionless()
        self.result = add
        return type(self)._from_dimensionless(self)

    def __sub__(self, other):
        sub = self._to_dimensionless() - other._to_dimensionless()
        self.result = sub
        return type(self)._from_dimensionless(self)

    def __mul__(self, other):
        if (isinstance(self, DimBase) and isinstance(other, DimBase)):
            raise Exception('Multiplication Not valid')

        else:
            mul = (other) * (self._to_dimensionless())
            self.result = mul
            return type(self)._from_dimensionless(self)

    def __rmul__(self, other):
        if (isinstance(self, DimBase) and isinstance(other, DimBase)):
            raise Exception('Multiplication Not valid')

        else:
            mul = (other) * (self._to_dimensionless())
            self.result = mul
            return type(self)._from_dimensionless(self)


    def __truediv__(self, other):
        if (isinstance(other,DimBase)):
            div = self._to_dimensionless() / other._to_dimensionless()
            return div
        else:
            div = (self._to_dimensionless()) / (other)
            self.result = div
            return type(self)._from_dimensionless(self)

    def __rtruediv__(self, other):
        raise Exception('Division not valid')

    def __pow__(self, other):
        raise Exception('Power operation is not valid')
        
    def __rpow__(self, other):
        raise Exception('Power operation is not valid')

    def __neg__(self):
        return self * -1

    def __pos__(self):
        if self < 0:
            return self * -1
        else:
            return self


    @property
    @abstractmethod
    def conversion_factor(self):
        pass


    def _to_dimensionless(self):
        return float(self.data * self.conversion_factor)


    def _from_dimensionless(self):
        x = self.result / self.conversion_factor
        return self.__class__(x)












