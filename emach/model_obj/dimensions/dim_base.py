from abc import abstractmethod, ABC


class DimBase(float, ABC):
    def __new__(cls, value):
        return float.__new__(cls, value)

    @property
    @abstractmethod
    def conversion_factor(self):
        pass

    def _to_dimensionless(self):
        return float(self) * self.conversion_factor

    def _from_dimensionless(self):
        x = float(self) / self.conversion_factor
        return self.__class__(x)


    def __neg__(self):
        return self * -1

    def __pos__(self):
        if self < 0:
            return self * -1
        else:
            return self
