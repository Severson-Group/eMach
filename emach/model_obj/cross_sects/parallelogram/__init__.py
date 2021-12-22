import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectParallelogram']


class CrossSectParallelogram(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for Parallelogram class. This function takes in
        arguments and saves the information passed to private variable to make
        them read-only
        Parameters
        ----------
        **kwargs : any
            DESCRIPTION. Keyword arguments provided to the initialization function.
            The following argument names have to be included in order for the code
            to execute: name, dim_l, dim_t, dim_theta, location.
        Returns
        -------
        None
        '''
        self._create_attr(kwargs)

        super()._validate_attr()
        self._validate_attr()

    @property
    def dim_l(self):
        return self._dim_l

    @property
    def dim_t(self):
        return self._dim_t

    @property
    def dim_theta(self):
        return self._dim_theta

    def draw(self, drawer):
        l = self.dim_l  # height of the parallelogram
        t = self.dim_t  # width of the parallelogram
        theta = DimRadian(self.dim_theta)  # angle of the parallelogram

        x = [0, l * np.cos(theta), l * np.cos(theta) + t / np.sin(theta), t / np.sin(theta)]

        y = [0, l * np.sin(theta), l * np.sin(theta), 0];

        z = np.array([x, y])

        coords = np.transpose(z)

        points = self.location.transform_coords(coords)

        # draw parallelogram

        side_1 = drawer.draw_line(points[0], points[1])
        side_2 = drawer.draw_line(points[1], points[2])
        side_3 = drawer.draw_line(points[2], points[3])
        side_4 = drawer.draw_line(points[3], points[0])

        x_coord = (l * np.cos(theta) + t / np.sin(theta)) / 2
        y_coord = l * np.sin(theta) / 2

        ic = np.array([[x_coord, y_coord]])
        inner_coord = self.location.transform_coords(ic)
        segments = [side_1, side_2, side_3, side_4]

        cs_token = CrossSectToken(inner_coord[0], segments)

        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_l, DimLinear):
            raise TypeError('dim_l is not of DimLinear')

        if not isinstance(self._dim_t, DimLinear):
            raise TypeError('dim_t is not of DimLinear')

        if not isinstance(self._dim_theta, DimAngular):
            raise TypeError('dim_theta is not of DimAngular')


