from dim_angular import DimAngular


class DimRadian(DimAngular):
    def __new__(cls, value):
        if type(value).__bases__[0] is DimAngular:
            value = value.to_radians()
        return DimAngular.__new__(cls, value)

    def to_degrees(self):
        return self*180/3.14

    def to_radians(self):
        return self
    
    


    # def _to_dimensionless(self):
    #     return float(self.data * 180/3.14)
    #
    # def _from_dimensionless(num1):
    #     x = num1*3.14/ 180
    #     return DimRadian(x)
