import numpy as np

from ...dimensions.dim_linear import DimLinear
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectHollowRect']


class CrossSectHollowRect(CrossSectBase):

    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for HollowCylinder class. This function takes in
        arguments and saves the information passed to private variable to make
        them read-only
        Parameters
        ----------
        **kwargs : any
            DESCRIPTION. Keyword arguments provided to the initialization funcntion.
            The following argument names have to be included in order for the code
            to execute: name, dim_t, dim_r_o, location. 
            
        Returns
        -------
        None
        '''
        self._create_attr(kwargs)

        super()._validate_attr()
        # self._validate_attr()

    @property
    def dim_t1(self):
        return self._dim_t1

    @property
    def dim_t2(self):
        return self._dim_t2

    @property
    def dim_t3(self):
        return self._dim_t3

    @property
    def dim_t4(self):
        return self._dim_t4

    @property
    def dim_w(self):
        return self._dim_w

    @property
    def dim_h(self):
        return self._dim_h

    def draw(self, drawer):

        w = self.dim_w
        h = self.dim_h
        t1 = self.dim_t1
        t2 = self.dim_t2
        t3 = self.dim_t3
        t4 = self.dim_t4
        axis = [type(w)(0), type(w)(0)]

        x_inner = [axis[0] + t3, axis[0] + t3, w - t1 + axis[0], w - t1 + axis[0]]
        y_inner = [axis[1] + t4, axis[1] + h - t2, h - t2 + axis[1], t4 + axis[1]]
        x_outer = [axis[0], axis[0], w + axis[0], w + axis[0]]
        y_outer = [axis[1], axis[1] + h, h + axis[1], axis[1]]

        inner_pts = [x_inner, y_inner]
        outer_pts = [x_outer, y_outer]

        # convert coordinates to a form of [[x1,y1]..]
        inner_pts = list(zip(*inner_pts))
        inner_pts = [list(sublist) for sublist in inner_pts]
        outer_pts = list(zip(*outer_pts))
        outer_pts = [list(sublist) for sublist in outer_pts]

        p_i = self.location.transform_coords(inner_pts)  # shift coordinates based on anchor and theta given in location
        p_o = self.location.transform_coords(outer_pts)

        # draw inner rectangle
        l_i1 = drawer.draw_line(p_i[0], p_i[1])
        l_i2 = drawer.draw_line(p_i[1], p_i[2])
        l_i3 = drawer.draw_line(p_i[2], p_i[3])
        l_i4 = drawer.draw_line(p_i[3], p_i[0])

        # draw outer rectangle
        l_o1 = drawer.draw_line(p_o[0], p_o[1])
        l_o2 = drawer.draw_line(p_o[1], p_o[2])
        l_o3 = drawer.draw_line(p_o[2], p_o[3])
        l_o4 = drawer.draw_line(p_o[3], p_o[0])

        # Compute coordinate inside the surface to extrude
        x_coord = w / 2
        y_coord = t4 / 2
        inner_coord = self.location.transform_coords([[x_coord, y_coord]])

        token = [l_i1, l_i2, l_i3, l_i4, l_o1, l_o2, l_o3, l_o4]  # compile tokens

        cs_token = CrossSectToken(inner_coord[0], token)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):

        if isinstance(self._dim_r_o, DimLinear):
            pass
        else:
            raise TypeError("dim_r_o not of type DimLinear")

        if isinstance(self._dim_t, DimLinear):
            pass
        else:
            raise TypeError("dim_t not of type DimLinear")
