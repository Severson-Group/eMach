# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:26:02 2021

@author: Martin Johnson
"""

import sys
sys.path.append("...")
import des_opt as do

class BSPMObjective1(do.Objective):
    def getObjectives(self,fullResults)->'tuple':
        raise NotImplementedError