from .dim_base import DimBase
from abc import abstractmethod, ABC


class DimAngular(DimBase, ABC):
    def __new__(cls, value):
        return DimBase.__new__(cls, value)

    @abstractmethod
    def _conversion_factor(self):
        pass
