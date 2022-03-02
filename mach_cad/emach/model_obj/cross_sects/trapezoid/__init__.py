import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectTrapezoid']


class CrossSectTrapezoid(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for Trapezoid class. This function takes in
        arguments and saves the information passed to private variable to make
        them read-only
        Parameters
        ----------
        **kwargs : any
            DESCRIPTION. Keyword arguments provided to the initialization funcntion.
            The following argument names have to be included in order for the code
            to execute: name, dim_h, dim_w, dim_theta, location.

        Returns
        -------
        None
        '''
        self._create_attr(kwargs)

        super()._validate_attr()
        self._validate_attr()

    @property
    def dim_h(self):
        return self._dim_h

    @property
    def dim_w(self):
        return self._dim_w

    @property
    def dim_theta(self):
        return self._dim_theta

    def draw(self, drawer):
        h = self.dim_h  # height of the trapezoid
        w = self.dim_w  # width of the trapezoid
        theta = DimRadian(self.dim_theta)  # angle of the trapezoid

        x = [-(w / 2), -(w / 2) + (h / np.tan(theta)), (w / 2) - (h / np.tan(theta)), (w / 2)]

        y = [0, h, h, 0]

        z = np.array([x, y])

        coords = np.transpose(z)

        p = self.location.transform_coords(coords)

        # Draw segments
        top_seg = drawer.draw_line(p[1], p[2])
        bottom_seg = drawer.draw_line(p[0], p[3])
        left_seg = drawer.draw_line(p[0], p[1])
        right_seg = drawer.draw_line(p[2], p[3])

        ic = np.array([[type(h)(0), h / 2]])
        inner_coord = self.location.transform_coords(ic)

        segments = [top_seg, bottom_seg, left_seg, right_seg]
        cs_token = CrossSectToken(inner_coord[0], segments)

        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_w, DimLinear):
            raise TypeError('dim_w is not of DimLinear')

        if not isinstance(self._dim_h, DimLinear):
            raise TypeError('dim_h is not of DimLinear')

        if not isinstance(self._dim_theta, DimAngular):
            raise TypeError('dim_theta is not of DimAngular')
