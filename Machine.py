# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:43:32 2021

@author: Martin Johnson
"""
from abc import ABC, abstractmethod

class Machine(ABC):
    """ABC for Machine objects"""
    @abstractmethod
    def __init__(self):
        pass
    
        
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MissingValueError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
