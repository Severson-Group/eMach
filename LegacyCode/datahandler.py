# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:28:09 2021

@author: Martin Johnson
"""
import sys
sys.path.append("..")
import desopt as do

class DataHandler(do.DataHandler):
    def save(self,design:'do.Design',fullResults,objs):
        raise NotImplementedError