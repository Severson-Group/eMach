
from abc import abstractmethod, ABC


class DimBase(float, ABC):
    def __new__(cls, value):
        return float.__new__(cls, value)
    def __init__(self,data):
        self.data = float(data)

    @property
    @abstractmethod
    def conversion_factor(self):
        pass

    def __pow__(self, other):
        raise Exception('Power operation is not valid')


    def _to_dimensionless(self):
        return float(self.data * self.conversion_factor)


    def _from_dimensionless(self):
        x = self.result / self.conversion_factor
        return self.__class__(x)












