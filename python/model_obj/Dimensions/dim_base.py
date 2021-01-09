
class DimBase(float):
    def __new__(cls, value):
        return float.__new__(cls, value)
    def __init__(self,data):
        self.data = float(data)










