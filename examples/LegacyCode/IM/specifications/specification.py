
from abc import ABC, abstractmethod


class Specification(ABC):
    """ABC which holds information on the specification of a machine"""
   
    @abstractmethod
    def __init__(self):
        """Create Specification class"""
        self.op_point: "OperatingPoint"
