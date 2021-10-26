import numpy as np

from .dimensions.dim_linear import DimLinear
from .dimensions.dim_angular import DimAngular
from .dimensions import *

__all__ = ['Location2D']


class Location2D():

    def __init__(self, anchor_xy=[DimMillimeter(0), DimMillimeter(0)], theta=DimRadian(0)):
        """
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

        """
        self._anchor_xy = anchor_xy
        self._theta = theta
        self._validate_attr()

        self._theta = DimRadian(theta)
        self._rot = np.array([[np.cos(self._theta), -np.sin(self._theta)],
                              [np.sin(self._theta), np.cos(self._theta)]])

    @property
    def anchor_xy(self):
        return self._anchor_xy

    @property
    def theta(self):
        return self._theta

    @property
    def rot(self):
        return self._rot

    def _validate_attr(self):

        if not len(self._anchor_xy) == 2:
            raise TypeError("Expected input to be one of length 2. \
                             Instead it was of length " + str(len(self._anchor_xy)))

        for i in range(len(self._anchor_xy)):
            if not isinstance(self._anchor_xy[i], DimLinear):
                raise TypeError("Expected input to be one of the following type: \
                             DimLinear. Instead it was of type " + str(type(self._anchor_xy[i])))

        if not isinstance(self._theta, DimAngular):
            raise TypeError("Expected input to be one of the following type: \
                             DimAngular. Instead it was of type " + str(type(self._theta)))

    def transform_coords(self, coords, add_theta=None):
        """
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
            DESCRIPTION. An nx2 array of coordinates of the form [x,y] transformed
            based on Location2D.__anchor_xy, Location2D.__anchor_xy and add_theta
        """
        coords_np = np.array(coords)  # convert coords to number for ease of calc
        if add_theta is None:
            trans = self._rot
        else:
            add_theta = DimRadian(add_theta) + self._theta
            trans = np.array([[np.cos(add_theta), -np.sin(add_theta)],
                              [np.sin(add_theta), np.cos(add_theta)]])
        rot_coords = np.transpose(np.matmul(trans, np.transpose(coords_np)))
        trans_coords = np.zeros(coords_np.shape)

        # need to convert numpy array to list to ensure dimension is conserved
        # all entries within numpy array default to type float64
        trans_coords_list = trans_coords.tolist()
        row, col = rot_coords.shape

        # add argument coords with anchor to get desired coordinates
        # convert type back to what it was before
        for i in range(row):
            trans_coords_list[i][0] = type(coords[i][0])(rot_coords[i, 0]) + self._anchor_xy[0]
            trans_coords_list[i][1] = type(coords[i][1])(rot_coords[i, 1]) + self._anchor_xy[1]
        return trans_coords_list
