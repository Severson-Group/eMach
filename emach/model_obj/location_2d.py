
import numpy as np

from .dimensions import DimMillimeter, DimRadian

__all__ = ['Location2D']
class Location2D():
    
    def __init__(self, anchor_xy = np.array([DimMillimeter(0), DimMillimeter(0)]), \
                 theta = DimRadian(0)):
        '''
        Initialization function for Location2D class. It assigns the value of 
        the arguments passed to private variables and creates a new variable
        __rot which holds the Park's transformation matrix corresponding to
        theta input'

        Parameters
        ----------
        anchor_xy : List of DimLinear objects
            DESCRIPTION. Distance from global xy coordinate to component's 
            origin xy coordinate. The default is np.array([0, 0]).
        theta : DimAngular
            DESCRIPTION. Angle about global xy axes to rotate component's xy
            axes. The default is 0.

        Returns
        -------
        None.

        '''
        self.__anchor_xy = anchor_xy; 
        self.__theta = DimRadian(theta);
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
        '''
        This function takes in an nx2 array of coordinates of the form [x,y] 
        and returns rotated and translated coordinates. The translation and 
        rotation are described by self.__anchor_xy and self.__theta. The optional 
        "addTheta" argument adds an additional angle of "addTheta" to the 
        self.__theta attribute.

        Parameters
        ----------
        coords : List of DimLinear
            DESCRIPTION. An nx2 array of coordinates of the form [x,y]
        add_theta : DimAngular, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        trans_coords : List of DimLinear
            DESCRIPTION. An nx2 array of coordinates of the form [x,y] tranformed
            based on Location2D.__anchor_xy, Location2D.__anchor_xy and add_theta

        '''
        if add_theta is None:
            trans = self.__rot
        else:
            add_theta = DimRadian(add_theta) + self.__theta
            trans = np.array([[np.cos(add_theta), -np.sin(add_theta)],
                                   [np.sin(add_theta), np.cos(add_theta)]])
        rot_coords = np.transpose(np.matmul(trans,np.transpose(coords)))
        trans_coords = np.zeros(coords.shape)

        trans_coords[:,0] = rot_coords[:,0] + self.__anchor_xy[0]
        trans_coords[:,1] = rot_coords[:,1] + self.__anchor_xy[1]
        return trans_coords
    
        
        