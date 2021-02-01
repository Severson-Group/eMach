from dim_linear import DimLinear



class DimInch(DimLinear):
    def __new__(cls, value):
        if type(value).__bases__[0] is DimLinear:
            value = value.to_inch()
        return DimLinear.__new__(cls, value)

    def to_mm(self):
        return self * 25.4

    def to_inch(self):
        return self
    
    @property
    def conversion_factor(self):
        return 25.4
    


