from .dim_base import DimBase

class DimAngular(DimBase):
    def __new__(cls, value):
        return DimBase.__new__(cls, value)

    def __init__(self, data):
        DimBase.__init__(self, data)
        

