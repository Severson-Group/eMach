import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimDegree
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectNotchedRectangle']


class CrossSectNotchedRectangle(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Notched Rectangle class. This function takes in
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
    def dim_w(self):
        return self._dim_w

    @property
    def dim_w_n(self):
        return self._dim_w_n

    @property
    def dim_d(self):
        return self._dim_d

    @property
    def dim_d_n(self):
        return self._dim_d_n

    def draw(self, drawer):
        w = self.dim_w
        w_n = self.dim_w_n
        d = self.dim_d
        d_n = self.dim_d_n

        x1 = 0
        x2 = w_n
        x3 = w - w_n
        x4 = w

        y1 = 0
        y2 = d
        y3 = d + d_n

        x = [x1, x4, x4, x3, x3, x2, x2, x1]
        y = [y1, y1, y3, y3, y2, y2, y3, y3]

        p = np.array([x, y])

        p = np.transpose(p)

        points = self.location.transform_coords(p)

        seg1 = drawer.draw_line(points[0], points[1])
        seg2 = drawer.draw_line(points[1], points[2])
        seg3 = drawer.draw_line(points[2], points[3])
        seg4 = drawer.draw_line(points[3], points[4])
        seg5 = drawer.draw_line(points[4], points[5])
        seg6 = drawer.draw_line(points[5], points[6])
        seg7 = drawer.draw_line(points[6], points[7])
        seg8 = drawer.draw_line(points[7], points[0])

        x_coord = w / 2
        y_coord = d / 2
        inner_coord = self.location.transform_coords(np.array([[x_coord, y_coord]]))

        segments = [seg1, seg2, seg3, seg4,seg5, seg6, seg7, seg8]

        cs_token = CrossSectToken(inner_coord[0], segments)  # create CrossSectToken object

        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_w, DimLinear):
            raise TypeError('dim_w is not of DimLinear')

        if not isinstance(self._dim_d, DimLinear):
            raise TypeError('dim_d is not of DimLinear')

        if not isinstance(self._dim_d_n, DimLinear):
            raise TypeError('dim_d_n is not of DimLinear')

        if not isinstance(self._dim_w_n, DimLinear):
            raise TypeError('dim_w_n is not of DimLinear')



