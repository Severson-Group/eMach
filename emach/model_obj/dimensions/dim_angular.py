from .dim_base import DimBase

class DimAngular(DimBase):
    def __new__(cls, value):
        return DimBase.__new__(cls, value)

    def __init__(self, data):
        DimBase.__init__(self, data)
        
    def __neg__(self):
        return self * -1

    def __pos__(self):
        if self < 0:
            return self * -1
        else:
            return self
