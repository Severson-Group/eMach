

from .dimensions import DimMillimeter, DimRadian
from .dimensions.dim_angular import DimAngular
from .dimensions.dim_linear import DimLinear

__all__ = ['Location3D']

class Location3D():
    def __init__(self, anchor_xyz = [DimMillimeter(0), DimMillimeter(0), DimMillimeter(0)], \
                 rotate_xyz = [DimRadian(0), DimRadian(0), DimRadian(0)]): 
        
        self._anchor_xyz = anchor_xyz  # Distance from global origin xyz coordinate to component's origin xyz coordinate
        self._rotate_xyz = rotate_xyz # Angles about global xyz axes to rotate component's xyz axes in radians
        
    @property
    def anchor_xyz(self):
        return self._anchor_xyz
    
    @property
    def rotate_xyz(self):
        return self._rotate_xyz
    
    def _validate_attr(self):
        
        if not len(self._anchor_xyz) == 3:
            raise TypeError ("Expected input to be one of length 3. \
                             Instead it was of length " + \
                             str(len(self._anchor_xyz)))
                
        for i in range(len(self._anchor_xyz)):
            if not isinstance(self.__anchor_xy[i],DimLinear):
                raise TypeError ("Expected input to be one of the following type: \
                             DimLinear. Instead it was of type " + \
                             str(type(self._anchor_xyz[i])))
        
        if not len(self._rotate_xyz) == 3:
            raise TypeError ("Expected input to be one of length 3. \
                             Instead it was of length " + \
                             str(len(self._rotate_xyz)))
                
        for i in range(len(self._rotate_xyz)):
            if not isinstance(self._rotate_xyz[i],DimAngular):
                raise TypeError ("Expected input to be one of the following type: \
                             DimAngular. Instead it was of type " + \
                             str(type(self._rotate_xyz[i])))
                
    