# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:48:15 2020

@author: Bharat
"""

from abc import ABC, abstractmethod

# define abstract base class for ToolBase
class ToolBase(ABC):
    @abstractmethod
    def open(self, filename, visible): pass
    
    @abstractmethod
    def close(self): pass

# define abstract base class for DrawerBase
class DrawerBase(ABC):
    @abstractmethod
    def draw_line(self, startxy, endxy): pass
    
    @abstractmethod
    def draw_arc(self, centerxy, startxy, endxy): pass

    @abstractmethod
    def select(self): pass

class MakerBase(ABC):
    @abstractmethod
    def prepare_section(self, inner_coord): pass

# define abstract base class for MakerExtrudeBase
class MakerExtrudeBase(MakerBase):
    @abstractmethod
    def extrude(self, name, material, depth, token): pass

# define abstract base class for MakerRevolveBase 
class MakerRevolveBase(MakerBase):
    @abstractmethod
    def revolve(self, name, material, center, axis, angle, token): pass