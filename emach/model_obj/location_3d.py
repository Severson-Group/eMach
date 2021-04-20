
import numpy as np

from .dimensions import DimMillimeter, DimRadian

__all__ = ['Location3D']

class Location3D():
    def __init__(self, anchor_xyz = np.array([DimMillimeter(0), DimMillimeter(0), DimMillimeter(0)]), \
                 rotate_xyz = np.array([DimRadian(0), DimRadian(0), DimRadian(0)])): 
        
        self._anchor_xyz = anchor_xyz  # Distance from global origin xyz coordinate to component's origin xyz coordinate
        self._rotate_xyz = rotate_xyz # Angles about global xyz axes to rotate component's xyz axes in radians
        
    @property
    def anchor_xyz(self):
        return self._anchor_xyz
    
    @property
    def rotate_xyz(self):
        return self._rotate_xyz