from abc import ABC, abstractmethod

class MakeSolidBase(ABC):
    
    @abstractmethod 
    def run(self, name, material, cs_token, maker):
        pass
    