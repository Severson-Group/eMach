
from abc import abstractmethod, ABC


class DimBase(float, ABC):
    def __new__(cls, value):
        return float.__new__(cls, value)
    def __init__(self,data):
        self.data = float(data)


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












