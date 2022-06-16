from abc import ABC, abstractmethod


class Analyzer(ABC):
    """This is the Analyzer ABC, it is used to extract results from a machine
    object. This is where the analysis of a machine in the optimization 
    process will occur.    
    """

    @abstractmethod
    def __init__(self):
        """Initialize Analyzer"""
        pass

    @abstractmethod
    def analyze(
        self, machine: "Machine", op_point: "OperatingPoint"
    ) -> "AnalysisResults":
        """This function takes in the machine to be analyzed, and an operating
        point, completes some calculation and returns an Evaluation Object
        
        Keyword Argument:
            machine: Machine
            op_point: Dict
            
        Return Value:
            analysis_results: AnalysisResults
        """
