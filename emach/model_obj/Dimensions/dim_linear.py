from .dim_base import DimBase



class DimLinear(DimBase):
    def __new__(cls, value):
        return DimBase.__new__(cls, value)

    def __init__(self, data):
        DimBase.__init__(self, data)

    def __add__(self, other):
        add = self._to_dimensionless() + other._to_dimensionless()
        self.result = add
        return type(self)._from_dimensionless(self)

    def __sub__(self, other):
        sub = self._to_dimensionless() - other._to_dimensionless()
        self.result = sub
        return type(self)._from_dimensionless(self)

    def __mul__(self, other):
        if (isinstance(self, DimLinear) and isinstance(other, DimLinear)):
            raise Exception('Multiplication Not valid')

        if isinstance(self, DimLinear):
            mul = (other) * (self._to_dimensionless())
            self.result = mul 
            return type(self)._from_dimensionless(self)

    def __rmul__(self, other):
        if (isinstance(self, DimLinear) and isinstance(other, DimLinear)):
            raise Exception('Multiplication Not valid')

        if isinstance(self, DimLinear):
            mul = (other) * (self._to_dimensionless())
            self.result = mul
            return type(self)._from_dimensionless(self)


    def __truediv__(self, other):
        if (isinstance(other,DimLinear)):
            div = self._to_dimensionless() / other._to_dimensionless()
            return div
        else:
            div = (self._to_dimensionless()) / (other)
            self.result = div
            return type(self)._from_dimensionless(self)

    def __rtruediv__(self, other):
        raise Exception('Division not valid')


    def __neg__(self):
        return self * -1

    def __pos__(self):
        if self < 0:
            return self * -1
        else:
            return self

        
