import numpy as np

from ...dimensions import DimRadian
from ...dimensions import DimMillimeter
from ...dimensions.dim_linear import DimLinear

from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectInnerRotorDropSlots', 'CrossSectInnerRotorDropSlotsBar']


class CrossSectInnerRotorDropSlots(CrossSectBase):

    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for CrossSectInnerRotorDropSlots class. This function takes in
        arguments and saves the information passed to private variable to make
        them read-only
        Parameters
        ----------
        **kwargs : any
            DESCRIPTION. Keyword arguments provided to the initialization funcntion.
            The following argument names have to be included in order for the code
            to execute:  name, dim_l, dim_t, dim_theta, location.
            
        Returns
        -------
        None
        '''
        self._create_attr(kwargs)

        super()._validate_attr()
        self._validate_attr()

    @property
    def dim_r_ri(self):
        return self._dim_r_ri

    @property
    def dim_d_ri(self):
        return self._dim_d_ri

    @property
    def dim_d_rb(self):
        return self._dim_d_rb

    @property
    def dim_r_rb1(self):
        return self._dim_r_rb1

    @property
    def dim_r_rb2(self):
        return self._dim_r_rb2

    @property
    def dim_d_so(self):
        return self._dim_d_so

    @property
    def dim_w_so(self):
        return self._dim_w_so

    @property
    def Qr(self):
        return self._Qr

    def draw(self, drawer):

        r_ri = self.dim_r_ri
        d_ri = self.dim_d_ri
        d_rb = self.dim_d_rb
        r_rb1 = self.dim_r_rb1
        r_rb2 = self.dim_r_rb2
        d_so = self.dim_d_so
        w_so = self.dim_w_so
        Qr = self.Qr

        alpha_u = DimRadian(2 * np.pi / Qr)
        r1 = r_ri + d_ri + r_rb2 + d_rb + DimMillimeter(np.sqrt(r_rb1 ** 2 - (w_so / 2) ** 2)) + d_so
        r2 = w_so / 2
        r_ro = DimMillimeter(np.sqrt(r1 ** 2 + r2 ** 2))

        x1 = r_ro * np.cos(alpha_u / 2)
        y1 = - r_ro * np.sin(alpha_u / 2)

        x2 = DimMillimeter(np.sqrt(r_ro ** 2 - (w_so / 2) ** 2))
        y2 = - w_so / 2

        x3 = x2 - d_so
        y3 = y2

        Rc2 = r_ri + d_ri + r_rb2
        Rc1 = Rc2 + d_rb

        alpha_slope = np.arcsin((r_rb1 - r_rb2) / d_rb)

        x4 = Rc1 - r_rb1 * np.sin(alpha_slope)
        y4 = - r_rb1 * np.cos(alpha_slope)

        x5 = Rc2 - r_rb2 * np.sin(alpha_slope)
        y5 = - r_rb2 * np.cos(alpha_slope)

        x6 = r_ri + d_ri
        y6 = DimMillimeter(0)

        x7 = x5
        y7 = - y5

        x8 = x4
        y8 = - y4

        x9 = x3
        y9 = - y3

        x10 = x2
        y10 = - y2

        x11 = x1
        y11 = - y1

        center_rotor_bar1 = [Rc1, DimMillimeter(0)]
        center_rotor_bar2 = [Rc2, DimMillimeter(0)]

        x_arr = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, center_rotor_bar1[0], center_rotor_bar2[0]]
        y_arr = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, center_rotor_bar1[1], center_rotor_bar2[1]]

        arc1 = []
        arc2 = []
        arc3 = []
        arc4 = []
        arc5 = []
        arc6 = []
        arc7 = []
        arc8 = []
        seg1 = []
        seg2 = []
        seg3 = []
        seg4 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(0, Qr):
            p = self.location.transform_coords(coords, alpha_u * i)

            arc1.append(drawer.draw_arc(self.location.anchor_xy, p[0], p[1]))
            seg1.append(drawer.draw_line(p[1], p[2]))
            arc2.append(drawer.draw_arc(p[11], p[3], p[2]))
            seg2.append(drawer.draw_line(p[3], p[4]))
            arc3.append(drawer.draw_arc(p[12], p[5], p[4]))
            arc4.append(drawer.draw_arc(p[12], p[6], p[5]))
            seg3.append(drawer.draw_line(p[6], p[7]))
            arc5.append(drawer.draw_arc(p[11], p[8], p[7]))
            seg4.append(drawer.draw_line(p[8], p[9]))
            arc6.append(drawer.draw_arc(self.location.anchor_xy, p[9], p[10]))

        arc7.append(drawer.draw_arc(self.location.anchor_xy,
            [r_ri, DimMillimeter(0)], [- r_ri, DimMillimeter(0)]))
        arc8.append(drawer.draw_arc(self.location.anchor_xy,
            [- r_ri, DimMillimeter(0)], [r_ri, DimMillimeter(0)]))

        rad = (r_ri + x6) / 2
        inner_coord = self.location.transform_coords([[rad, 0]])
        segments = [arc1, seg1, arc2, seg2, arc3, arc4, seg3, arc5, seg4, arc6, arc7, arc8]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)
        return cs_token

    def _validate_attr(self):

        if isinstance(self._dim_r_ri, DimLinear):
            pass
        else:
            raise TypeError("dim_r_ri not of type DimLinear")

        if isinstance(self._dim_d_ri, DimLinear):
            pass
        else:
            raise TypeError("dim_d_ri not of type DimLinear")

        if isinstance(self._dim_d_rb, DimLinear):
            pass
        else:
            raise TypeError("dim_d_rb not of type DimLinear")

        if isinstance(self._dim_r_rb1, DimLinear):
            pass
        else:
            raise TypeError("dim_r_rb1 not of type DimLinear")

        if isinstance(self._dim_r_rb2, DimLinear):
            pass
        else:
            raise TypeError("dim_r_rb2 not of type DimLinear")

        if isinstance(self._dim_d_so, DimLinear):
            pass
        else:
            raise TypeError("dim_d_so not of type DimLinear")

        if isinstance(self._dim_w_so, DimLinear):
            pass
        else:
            raise TypeError("dim_w_so not of type DimLinear")

        if isinstance(self._Qr, int):
            pass
        else:
            raise TypeError("Qr not of type int")



class CrossSectInnerRotorDropSlotsBar(CrossSectBase):

    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for RoundBar class. This function takes in
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
    def rotor_core(self):
        return self._rotor_core

    def draw(self, drawer):

        r_ri = self.rotor_core.dim_r_ri
        d_ri = self.rotor_core.dim_d_ri
        d_rb = self.rotor_core.dim_d_rb
        r_rb1 = self.rotor_core.dim_r_rb1
        r_rb2 = self.rotor_core.dim_r_rb2
        d_so = self.rotor_core.dim_d_so
        w_so = self.rotor_core.dim_w_so
        Qr = self.rotor_core.Qr

        alpha_u = DimRadian(2 * np.pi / Qr)
        r1 = r_ri + d_ri + r_rb2 + d_rb + DimMillimeter(np.sqrt(r_rb1 ** 2 - (w_so / 2) ** 2)) + d_so
        r2 = w_so / 2
        r_ro = DimMillimeter(np.sqrt(r1 ** 2 + r2 ** 2))

        x1 = r_ro * np.cos(alpha_u / 2)
        y1 = - r_ro * np.sin(alpha_u / 2)

        x2 = DimMillimeter(np.sqrt(r_ro ** 2 - (w_so / 2) ** 2))
        y2 = - w_so / 2

        x3 = x2 - d_so
        y3 = y2

        Rc2 = r_ri + d_ri + r_rb2
        Rc1 = Rc2 + d_rb

        alpha_slope = np.arcsin((r_rb1 - r_rb2) / d_rb)

        x4 = Rc1 - r_rb1 * np.sin(alpha_slope)
        y4 = - r_rb1 * np.cos(alpha_slope)

        x5 = Rc2 - r_rb2 * np.sin(alpha_slope)
        y5 = - r_rb2 * np.cos(alpha_slope)

        x6 = r_ri + d_ri
        y6 = DimMillimeter(0)

        x7 = x5
        y7 = - y5

        x8 = x4
        y8 = - y4

        x9 = x3
        y9 = - y3

        x10 = x2
        y10 = - y2

        x11 = x1
        y11 = - y1

        x12 = Rc1 + r_rb1
        y12 = DimMillimeter(0)

        center_rotor_bar1 = [Rc1, DimMillimeter(0)]
        center_rotor_bar2 = [Rc2, DimMillimeter(0)]

        x_arr = [x12, x4, x5, x6, x7, x8, center_rotor_bar1[0], center_rotor_bar2[0]]
        y_arr = [y12, y4, y5, y6, y7, y8, center_rotor_bar1[1], center_rotor_bar2[1]]

        arc1 = []
        seg1 = []
        arc2 = []
        arc3 = []
        seg2 = []
        arc4 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        p = self.location.transform_coords(coords, 0)

        arc1.append(drawer.draw_arc(p[6], p[1], p[0]))
        seg1.append(drawer.draw_line(p[1], p[2]))
        arc1.append(drawer.draw_arc(p[7], p[3], p[2]))
        arc3.append(drawer.draw_arc(p[7], p[4], p[3]))
        seg2.append(drawer.draw_line(p[4], p[5]))
        arc4.append(drawer.draw_arc(p[6], p[0], p[5]))

        inner_coord = self.location.transform_coords([center_rotor_bar1])
        segments = [arc1, seg1, arc2, arc3, seg2, arc4]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)

        return cs_token

    def _validate_attr(self):

        if isinstance(self.rotor_core, CrossSectInnerRotorDropSlots):
            pass
        else:
            raise TypeError("rotor_core not of type CrossSectInnerRotorDropSlots")
