# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:48:15 2020

@author: Bharat
"""

from abc import ABC, abstractmethod

# define abstract base class for ToolBase
class ToolBase(ABC):
    @abstractmethod
    def open(self): pass
    
    @abstractmethod
    def close(self): pass

# define abstract base class for DrawerBase
class DrawerBase(ABC):
    @abstractmethod
    def drawLine(self): pass
    
    @abstractmethod
    def drawArc(self): pass

    @abstractmethod
    def select(self): pass

class MakerBase(ABC):
    @abstractmethod
    def prepareSection(self): pass

# define abstract base class for MakerExtrudeBase
class MakerExtrudeBase(MakerBase):
    @abstractmethod
    def extrude(self): pass

# define abstract base class for MakerRevolveBase 
class MakerRevolveBase(MakerBase):
    @abstractmethod
    def revolve(self): pass