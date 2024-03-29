import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectInnerNotchedRotor']


class CrossSectInnerNotchedRotor(CrossSectBase):

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
        self._validate_attr()

    @property
    def dim_alpha_rm(self):
        return self._dim_alpha_rm

    @property
    def dim_alpha_rs(self):
        return self._dim_alpha_rs

    @property
    def dim_r_ri(self):
        return self._dim_r_ri

    @property
    def dim_d_ri(self):
        return self._dim_d_ri

    @property
    def dim_d_rp(self):
        return self._dim_d_rp

    @property
    def dim_d_rs(self):
        return self._dim_d_rs

    @property
    def p(self):
        return self._p

    @property
    def s(self):
        return self._s

    def draw(self, drawer):

        alpha_rm = DimRadian(self._dim_alpha_rm)
        alpha_rs = DimRadian(self._dim_alpha_rs)
        r_ri = self._dim_r_ri
        d_ri = self._dim_d_ri
        d_rp = self._dim_d_rp
        d_rs = self._dim_d_rs
        p = self._p
        s = self._s
        P = 2 * p
        alpha_rp = DimRadian(2 * np.pi / P)
        try:
            alpha_k = (alpha_rm - (alpha_rs * s)) / (s - 1)
        except ZeroDivisionError:
            alpha_k = alpha_rs

        # Compute angles of various rotor segment start and end points
        if s % 2 == 1:
            prev_theta_m = alpha_rs / -2
            prev_theta_ms = DimRadian(0)
            angle = [0] * (s + 1)
            for i in range(0, s + 1):
                if i % 2 == 0:
                    theta_m = prev_theta_m + alpha_rs
                    prev_theta_m = theta_m
                else:
                    theta_ms = prev_theta_ms + alpha_k
                    prev_theta_ms = theta_ms

            angle[i] = prev_theta_m + prev_theta_ms

        else:
            prev_theta_ms = -alpha_k / 2
            prev_theta_m = 0
            angle = [0] * (s + 1)
            for i in range(0, s + 1):
                if i % 2 == 1:
                    theta_m = prev_theta_m + alpha_rs
                    prev_theta_m = theta_m
                else:
                    theta_ms = prev_theta_ms + alpha_k
                    prev_theta_ms = theta_ms

                angle[i] = prev_theta_m + prev_theta_ms

        # Assign angle for the end point of the interpolar segment
        angle[-1] = angle[-2] + (alpha_rp - alpha_rm)

        # Generate coordinates based on the points angles
        a = [0] * (s + 1)
        y = [0] * (s + 1)
        x = [0] * (s + 1)
        zx = [0] * (s + 1)
        zy = [0] * (s + 1)
        for i in range(0, s + 1):
            if i <= s - 2:
                a[i] = r_ri + d_ri + d_rs
            else:
                a[i] = r_ri + d_ri + d_rp

            y[i] = a[i] * np.sin(angle[i])
            x[i] = a[i] * np.cos(angle[i])
            zx[i] = (r_ri + d_ri) * np.cos((angle[i]))
            zy[i] = (r_ri + d_ri) * np.sin((angle[i]))

        # Reshape the coordinates for drawing

        flip_x = x[::-1]
        flip_x = flip_x[1:]
        x_array = flip_x + x

        flip_y = [y_ar * -1 for y_ar in y[::-1]]
        flip_y = flip_y[1:]
        y_array = flip_y + y

        flip_zx = zx[::-1]
        flip_zx = flip_zx[1:]
        zx_array = flip_zx + zx

        flip_zy = [zy_ar * -1 for zy_ar in zy[::-1]]
        flip_zy = flip_zy[1:]
        zy_array = flip_zy + zy
        points = []
        inner_points = []
        for index in range(0, len(x_array)):
            points.append([x_array[index], y_array[index]])
            inner_points.append([zx_array[index], zy_array[index]])
        # Draw p poles with s segments per pole
        arc = []
        lines = []
        for i in range(1, P + 1):
            points = self.location.transform_coords(points, DimRadian(2 * np.pi / P))
            inner_points = self.location.transform_coords(inner_points, DimRadian(2 * np.pi / P))
            for j in range(0, 2 * s + 1):
                if j % 2 == 1:
                    arc.append(drawer.draw_arc(self.location.anchor_xy, points[j], points[j + 1]))
                    lines.append(drawer.draw_line(points[j], inner_points[j]))

                if j % 2 == 0 and j < (2 * s):
                    arc.append(drawer.draw_arc(self.location.anchor_xy, inner_points[j], inner_points[j + 1]))
                    lines.append(drawer.draw_line(points[j], inner_points[j]))

                # Draw inner surface
        if r_ri == 0:
            point_i = self.location.anchor_xy
            inner_coord = self.location.transform_coords([point_i])
            segs = [x for segment in [arc, lines] for x in segment]
            cs_token = CrossSectToken(inner_coord[0], segs)

        else:
            point_i = [r_ri, 0] + self.location.anchor_xy
            point_i2 = [-r_ri, 0] + self.location.anchor_xy
            print(type(point_i2[0]))
            arc_i1 = drawer.draw_arc(self.location.anchor_xy, point_i, point_i2)
            arc_i2 = drawer.draw_arc(self.location.anchor_xy, point_i2, point_i)
            rad = r_ri + d_ri
            inner_coord = self.location.transform_coords([[rad, type(r_ri)(0)]])
            segments = [arc, lines, [arc_i1], [arc_i2]]

            segs = [x for segment in segments for x in segment]
            cs_token = CrossSectToken(inner_coord[0], segs)

        return cs_token

    def _validate_attr(self):

        if isinstance(self._dim_alpha_rm, DimAngular):
            pass
        else:
            raise TypeError("dim_alpha_rm not of type DimAngular")

        if isinstance(self._dim_alpha_rs, DimAngular):
            pass
        else:
            raise TypeError("dim_alpha_rs not of type DimAngular")

        if isinstance(self._dim_r_ri, DimLinear):
            pass
        else:
            raise TypeError("dim_r_ri not of type DimLinear")

        if isinstance(self._dim_d_ri, DimLinear):
            pass
        else:
            raise TypeError("dim_d_ri not of type DimLinear")

        if isinstance(self._dim_d_rp, DimLinear):
            pass
        else:
            raise TypeError("dim_d_rp not of type DimLinear")

        if isinstance(self._dim_d_rs, DimLinear):
            pass
        else:
            raise TypeError("dim_d_rs not of type DimLinear")

        if isinstance(self._s, int):
            pass
        else:
            raise TypeError("s not of type int")

        if isinstance(self._p, int):
            pass
        else:
            raise TypeError("p not of type int")
