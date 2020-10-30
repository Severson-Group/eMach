# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 20:50:52 2020

@author: Bharat
"""
from . import document
from . import view

from .document import*
from .view import*

__all__ = []
__all__ += document.__all__
__all__ += view.__all__
