from typing import Union, Protocol, runtime_checkable
from abc import abstractmethod
import numpy as np


@runtime_checkable
class BField(Protocol):
    """Protocol for analyzer field classes"""

    @abstractmethod
    def radial(
        self, alpha: np.array, r: Union[int, float], harmonics: np.array
    ) -> np.array:
        pass

    @abstractmethod
    def tan(
        self, alpha: np.array, r: Union[int, float], harmonics: np.array
    ) -> np.array:
        pass
