from typing import Protocol
from abc import abstractmethod

class PostAnalyzer(Protocol):
    @abstractmethod
    def get_next_state(self,results:'Results',stateIn:'State')->'State':
        pass