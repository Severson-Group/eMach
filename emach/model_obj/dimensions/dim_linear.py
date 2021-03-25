from .dim_base import DimBase


class DimLinear(DimBase):
    def __new__(cls, value):
        return DimBase.__new__(cls, value)


