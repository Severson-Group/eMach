# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:18:33 2021

@author: Martin Johnson
"""

import sys
sys.path.append("...")
import macheval as me
from typing import Any
from copy import deepcopy

class LengthScaleStep(me.EvaluationStep):
    
    def __init__(self,settings):
        pass
    
    def step(self,stateIn:'me.State')->[Any,'me.State']:
        pass