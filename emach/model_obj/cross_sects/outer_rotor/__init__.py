import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimDegree
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectOuterRotor']


class CrossSectOuterRotor(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Outer Rotor class. This function takes in
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
    def dim_alpha_rs(self):
        return self._dim_alpha_rs

    @property
    def dim_alpha_rm(self):
        return self._dim_alpha_rm

    @property
    def dim_r_ro(self):
        return self._dim_r_ro

    @property
    def dim_d_rp(self):
        return self._dim_d_rp

    @property
    def dim_d_ri(self):
        return self._dim_d_ri

    @property
    def dim_d_rs(self):
        return self._dim_d_rs

    @property
    def dim_p(self):
        return self._dim_p

    @property
    def dim_S(self):
        return self._dim_S

    def draw(self, drawer):
        alpha_rs = DimRadian(self.dim_alpha_rs)
        alpha_rm = DimRadian(self.dim_alpha_rm)
        r_ro = self.dim_r_ro
        d_rp = self.dim_d_rp
        d_ri = self.dim_d_ri
        d_rs = self.dim_d_rs
        pole_pair = self.dim_p
        segments = self.dim_S

        alpha_total = DimRadian(DimDegree(180 / pole_pair))

        # outer arc
        r = r_ro
        x1 = r * np.cos(alpha_total / 2)
        y1 = r * np.sin(alpha_total / 2)

        # inner arc between poles
        r = r_ro - d_ri - d_rp
        x2 = r * np.cos(alpha_rm / 2)
        y2 = r * np.sin(alpha_rm / 2)
        x3 = r * np.cos(alpha_total / 2)
        y3 = r * np.sin(alpha_total / 2)

        # line containing region between poles
        r = r_ro - d_ri
        x4 = r * np.cos(alpha_rm / 2)
        y4 = r * np.sin(alpha_rm / 2)

        x_arr = [x1, x1, x2, x3, x2, x3, x4, x4]
        y_arr = [y1, -y1, y2, y3, -y2, -y3, y4, -y4]

        if segments > 1:
            raise NotImplementedError("S > 1 not supported")

        points = np.array([x_arr, y_arr])

        points = np.transpose(points)

        arc1 = []
        arc2 = []
        arc3 = []
        arc4 = []

        seg1 = []
        seg2 = []

        for i in range(2 * pole_pair):
            angle = alpha_total * i
            points_transformed = self.location.transform_coords(points, DimRadian(angle))

            x = points_transformed[:, 0]
            y = points_transformed[:, 1]

            p1 = [x[0], y[0]]
            p2 = [x[1], y[1]]

            p3 = [x[2], y[2]]
            p4 = [x[3], y[3]]

            p5 = [x[4], y[4]]
            p6 = [x[5], y[5]]

            p7 = [x[6], y[6]]
            p8 = [x[7], y[7]]

            arc1.append(drawer.draw_arc(self.location.anchor_xy, p2, p1))
            arc2.append(drawer.draw_arc(self.location.anchor_xy, p3, p4))
            arc3.append(drawer.draw_arc(self.location.anchor_xy, p6, p5))

            seg1.append(drawer.draw_line(p3, p7))
            seg2.append(drawer.draw_line(p5, p8))

            arc4.append(drawer.draw_arc(self.location.anchor_xy, p8, p7))

        rad = r_ro - (d_ri / 2);
        ic = np.array([[rad, type(rad)(0)]])
        inner_coord = self.location.transform_coords(np.array(ic))
        data = [arc1]
        cs_token = CrossSectToken(inner_coord[0, :], data)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):
        if not isinstance(self._dim_alpha_rs, DimAngular):
            raise TypeError('dim_alpha_rs is not of DimAngular')

        if not isinstance(self._dim_alpha_rm, DimAngular):
            raise TypeError('dim_alpha_rm is not of DimAngular')

        if not isinstance(self._dim_r_ro, DimLinear):
            raise TypeError('dim_r_ro is not of DimLinear')

        if not isinstance(self._dim_d_rp, DimLinear):
            raise TypeError('dim_d_rp is not of DimLinear')

        if not isinstance(self._dim_d_ri, DimLinear):
            raise TypeError('dim_d_ri is not of DimLinear')

        if not isinstance(self._dim_d_rs, DimLinear):
            raise TypeError('dim_d_rs is not of DimLinear')

        if not isinstance(self._dim_p, int):
            raise TypeError('dim_p is not of int')

        if not isinstance(self._dim_S, int):
            raise TypeError('dim_S is not of int')


