# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:48:15 2020

@author: Bharat
"""

from abc import ABC, abstractmethod
from typing import List

from ...model_obj import Location2D


# define abstract base class for ToolBase
class ToolBase(ABC):
    @abstractmethod
    def open(self, filename: str, visible: bool) -> None: pass
    
    @abstractmethod
    def close(self): pass

# define abstract base class for DrawerBase
class DrawerBase(ABC):
    @abstractmethod
    def draw_line(self, startxy: Location2D, endxy: Location2D) -> int: pass
    
    @abstractmethod
    def draw_arc(self, centerxy: Location2D, startxy: Location2D, 
                 endxy: Location2D) -> int: pass

    @abstractmethod
    def select(self): pass

class MakerBase(ABC):
    @abstractmethod
    def prepare_section(self, inner_coord: Location2D) -> None: pass

# define abstract base class for MakerExtrudeBase
class MakerExtrudeBase(MakerBase):
    @abstractmethod
    def extrude(self, name: List[str], material: str, depth: float, token) -> int: pass

# define abstract base class for MakerRevolveBase 
class MakerRevolveBase(MakerBase):
    @abstractmethod
    def revolve(self, name: List[str], material: str, center: Location2D, 
                axis: Location2D, angle: float, token): pass