import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimDegree
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectOuterRotorStator']


class CrossSectOuterRotorStator(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Outer Rotor Stator class. This function takes in
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
    def dim_alpha_st(self):
        return self._dim_alpha_st

    @property
    def dim_alpha_so(self):
        return self._dim_alpha_so

    @property
    def dim_r_si(self):
        return self._dim_r_si

    @property
    def dim_d_so(self):
        return self._dim_d_so

    @property
    def dim_d_sp(self):
        return self._dim_d_sp

    @property
    def dim_d_st(self):
        return self._dim_d_st

    @property
    def dim_d_sy(self):
        return self._dim_d_sy

    @property
    def dim_w_st(self):
        return self._dim_w_st

    @property
    def dim_r_st(self):
        return self._dim_r_st

    @property
    def dim_r_sf(self):
        return self._dim_r_sf

    @property
    def dim_r_sb(self):
        return self._dim_r_sb

    @property
    def dim_Q(self):
        return self._dim_Q

    def draw(self, drawer):
        alpha_st = self.dim_alpha_st
        alpha_so = self.dim_alpha_so
        r_si = self.dim_r_si
        d_so = self.dim_d_so
        d_sp = self.dim_d_sp
        d_st = self.dim_d_st
        d_sy = self.dim_d_sy
        w_st = self.dim_w_st
        r_st = self.dim_r_st
        r_sf = self.dim_r_sf
        r_sb = self.dim_r_sb
        Q = self.dim_Q

        alpha_total = DimDegree(360 / Q).toRadians()

        # Inner Arc
        x1 = r_si * np.cos(alpha_total / 2)
        y1 = r_si * np.sin(alpha_total / 2)

        # Outer arc on tooth
        r = r_si + d_sy + d_st + d_sp
        x2 = r * np.cos(alpha_st / 2)
        y2 = r * np.sin(alpha_st / 2)

        # Outer wall arc(above tooth[below is mirror])
        r = r_si + d_sy
        x3 = r * np.cos(alpha_total / 2)  # top point
        y3 = r * np.sin(alpha_total / 2)  # top point

        phi = np.arcsin((w_st / 2) / r)
        x4 = r * np.cos(phi)  # lower point(still above x - axis)
        y4 = r * np.sin(phi)  # lower point(still above x - axis)

        # Tooth horizontal line outer point
        r = r_si + d_sy + d_st
        phi = np.arcsin((w_st / 2) / r)
        x5 = r * np.cos(phi)  # lower point(still above x - axis)
        y5 = r * np.sin(phi)  # lower point(still above x - axis)

        # Left point of d_so line
        theta = alpha_st / 2
        phi = DimDegree(180).toRadians() - alpha_so + theta
        L = r_si + d_sy + d_st + d_sp
        R = d_so
        x6 = L * np.cos(theta) + R * np.cos(phi)
        y6 = L * np.sin(theta) + R * np.sin(phi)

        x_arr = [x1, x1, x2, x2, x3, x4, x3, x4, x5, x5, x6, x6]
        y_arr = [y1, -y1, y2, -y2, y3, y4, -y3, -y4, y5, -y5, y6, -y6]

        x_arr_transpose = np.transpose(x_arr)
        y_arr_transpose = np.transpose(y_arr)

        arc1 = []
        arc2 = []
        arc3 = []
        arc4 = []

        seg1 = []
        seg2 = []
        seg3 = []
        seg4 = []
        seg5 = []
        seg6 = []

        for i in Q:
            p = obj.location.transformCoords([x_arr_transpose, y_arr_transpose], DimRadian((i - 1) * alpha_total));

            x = p[:, 1]
            y = p[:, 2]

            p1 = [x(2), y(2)]
            p2 = [x(1), y(1)]

            p3 = [x(4), y(4)]
            p4 = [x(3), y(3)]

            p5 = [x(6), y(6)]
            p6 = [x(5), y(5)]

            p7 = [x(7), y(7)]
            p8 = [x(8), y(8)]

            p9 = [x(9), y(9)]
            p10 = [x(10), y(10)]

            p11 = [x(11), y(11)]
            p12 = [x(12), y(12)]

            arc1.append(drawer.drawArc(obj.location.anchor_xy, p1, p2))
            arc2.append(drawer.drawArc(obj.location.anchor_xy, p3, p4))
            arc3.append(drawer.drawArc(obj.location.anchor_xy, p5, p6))
            arc4.append(drawer.drawArc(obj.location.anchor_xy, p7, p8))

            seg1.append(drawer.drawLine(p5, p9))
            seg2.append(drawer.drawLine(p8, p10))
            seg3.append(drawer.drawLine(p4, p11))
            seg4.append(drawer.drawLine(p3, p12))
            seg5.append(drawer.drawLine(p11, p9))
            seg6.append(drawer.drawLine(p12, p10))
        end

    def _validate_attr(self):

        if not isinstance(self._dim_alpha_st, DimAngular):
            raise TypeError('dim_alpha_st is not of DimAngular')

        if not isinstance(self._dim_alpha_so, DimAngular):
            raise TypeError('dim_alpha_so is not of DimAngular')

        if not isinstance(self._dim_r_si, DimLinear):
            raise TypeError('dim_r_si is not of DimLinear')

        if not isinstance(self._dim_d_so, DimLinear):
            raise TypeError('dim_d_so is not of DimLinear')

        if not isinstance(self._dim_d_sp, DimLinear):
            raise TypeError('dim_d_sp is not of DimLinear')

        if not isinstance(self._dim_d_st, DimLinear):
            raise TypeError('dim_d_st is not of DimLinear')

        if not isinstance(self._dim_d_sy, DimLinear):
            raise TypeError('dim_d_sy is not of DimLinear')

        if not isinstance(self._dim_w_st, DimLinear):
            raise TypeError('dim_w_st is not of DimLinear')

        if not isinstance(self._dim_r_st, DimLinear):
            raise TypeError('dim_r_st is not of DimLinear')

        if not isinstance(self._dim_r_sf, DimLinear):
            raise TypeError('dim_r_sf is not of DimLinear')

        if not isinstance(self._dim_r_sb, DimLinear):
            raise TypeError('dim_r_sb is not of DimLinear')

        if not isinstance(self._dim_Q, float):
            raise TypeError('dim_Q is not of float')
