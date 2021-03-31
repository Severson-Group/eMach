
__all__ = ['Location3D']

class Location3D():
    def __init__(self, anchor_xyz, rotate_xyz):
        self._anchor_xyz = anchor_xyz
        self._rotate_xyz = rotate_xyz
        
    @property
    def anchor_xyz(self):
        return self._anchor_xyz
    
    @property
    def rotate_xyz(self):
        return self._rotate_xyz