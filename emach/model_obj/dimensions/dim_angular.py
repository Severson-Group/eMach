from .dim_base import DimBase

from abc import abstractmethod, ABC

class DimAngular(DimBase,ABC):
    def __new__(cls, value):
        return DimBase.__new__(cls, value)
    def __init__(self, data):
        DimBase.__init__(self, data)


    @abstractmethod
    def to_degrees(self):
        pass

    @abstractmethod
    def to_radians(self):
        pass