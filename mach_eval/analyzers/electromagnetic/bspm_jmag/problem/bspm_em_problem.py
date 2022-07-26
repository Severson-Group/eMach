# from .architects.machines.bspm_machine import BSPM_Machine 

class BSPM_EM_Problem():
    def __init__(self, machine, operating_point):
        self.machine = machine
        self.operating_point = operating_point
        # self._validate_attr()
        
    # def _validate_attr(self):
    #     if (type(self.machine) is BSPM_Machine):
    #         pass
    #     else:
    #         raise TypeError    
        