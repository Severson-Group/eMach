# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 23:22:49 2020

@author: Bharat
"""
from abc import ABC, abstractmethod


class CrossSectBase(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def create_props(self):
        pass


class CrossSectToken:
    def __init__(self, inner_coord, token):
        self.inner_coord = inner_coord
        self.token = token
