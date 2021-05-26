import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectSolidRectangle']


class CrossSectSolidRectangle(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for Solid Rectangle class. This function takes in
        arguments and saves the information passed to private variable to make
        them read-only
        Parameters
        ----------
        **kwargs : any
            DESCRIPTION. Keyword arguments provided to the initialization function.
            The following argument names have to be included in order for the code
            to execute: name, dim_h, dim_w, location.
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

    def draw(self, drawer):
        h = self.dim_h  # height of the rectangle
        w = self.dim_w  # width of the rectangle

        axis = [type(w)(0), type(w)(0)]
        x = [axis[0], axis[0], axis[0] + w, axis[0] + w]
        y = [axis[1], axis[1]+h, axis[1] + h, axis[1]]

        p = np.array([x, y])

        p = np.transpose(p)

        points = self.location.transform_coords(p)

        # Draw Rectangle
        side_1 = drawer.draw_line(points[0, :], points[1, :])
        side_2 = drawer.draw_line(points[1, :], points[2, :])
        side_3 = drawer.draw_line(points[2, :], points[3, :])
        side_4 = drawer.draw_line(points[3, :], points[0, :])

        # Compute coordinate inside the surface to extrude
        x_coord = w / 2
        y_coord = h / 2
        inner_coord = self.location.transform_coords(np.array([[x_coord, y_coord]]))

        token = [side_1, side_2, side_3, side_4]  # compile tokens

        cs_token = CrossSectToken(inner_coord[0, :], token)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_w, DimLinear):
            raise TypeError('dim_w is not of DimLinear')

        if not isinstance(self._dim_h, DimLinear):
            raise TypeError('dim_h is not of DimLinear')
