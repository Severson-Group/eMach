# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 23:35:50 2020

@author: Bharat
"""
import numpy as np
__all__ = ['Location2D']

class Location2D():
    
    def __init__(self, anchor_xy = np.array([0, 0]), theta = 0):
        self.__anchor_xy = anchor_xy;
        self.__theta = theta * np.pi/180;
        self.__rot = np.array([[np.cos(self.__theta), -np.sin(self.__theta)],
                             [np.sin(self.__theta), np.cos(self.__theta)]])
    
    @property
    def anchor_xy(self):
        return self.__anchor_xy
    
    @property
    def theta(self):
        return self.__theta
    
    @property
    def rot(self):
        return self.__rot
    
    def trans_coord(self, coords, add_theta = None):
        if add_theta is None:
            trans = self.__rot
        else:
            add_theta = add_theta*np.pi/180 + self.__theta
            trans = np.array([[np.cos(add_theta), -np.sin(add_theta)],
                                   [np.sin(add_theta), np.cos(add_theta)]])
        rot_coords = np.transpose(np.matmul(trans,np.transpose(coords)))
        trans_coords = np.zeros(coords.shape)

        trans_coords[:,0] = rot_coords[:,0] + self.__anchor_xy[0]
        trans_coords[:,1] = rot_coords[:,1] + self.__anchor_xy[1]
        return trans_coords
    
        
        