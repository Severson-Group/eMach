import numpy as np

from ...dimensions import DimRadian
from ...dimensions import DimMillimeter
from ...dimensions.dim_linear import DimLinear

from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectInnerRotorRoundSlots', 'CrossSectInnerRotorRoundSlotsPartial', 'CrossSectInnerRotorRoundSlotsBar']


class CrossSectInnerRotorRoundSlots(CrossSectBase):

    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for CrossSectInnerRotorRoundSlots class. This function takes in
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
    def dim_r_rb(self):
        return self._dim_r_rb

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
        r_rb = self.dim_r_rb
        d_so = self.dim_d_so
        w_so = self.dim_w_so
        Qr = self.Qr

        alpha_u = DimRadian(2 * np.pi / Qr)
        r1 = r_ri + d_ri + r_rb + DimMillimeter(np.sqrt(r_rb ** 2 - (w_so / 2) ** 2)) + d_so
        r2 = w_so / 2
        r_ro = DimMillimeter(np.sqrt(r1 ** 2 + r2 ** 2))

        x1 = r_ro * np.cos(alpha_u / 2)
        y1 = - r_ro * np.sin(alpha_u / 2)

        x2 = DimMillimeter(np.sqrt(r_ro ** 2 - (w_so / 2) ** 2))
        y2 = - w_so / 2

        x3 = x2 - d_so
        y3 = y2

        x4 = r_ri + d_ri
        y4 = DimMillimeter(0)

        x5 = x3
        y5 = - y3

        x6 = x2
        y6 = - y2

        x7 = x1
        y7 = - y1

        center_rotor_bar = [(x4 + r_rb), DimMillimeter(0)]

        x_arr = [x1, x2, x3, x4, x5, x6, x7, center_rotor_bar[0]]
        y_arr = [y1, y2, y3, y4, y5, y6, y7, center_rotor_bar[1]]

        arc1 = []
        arc2 = []
        arc3 = []
        arc4 = []
        arc5 = []
        arc6 = []
        seg1 = []
        seg2 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(0, Qr):
            p = self.location.transform_coords(coords, alpha_u * i)

            arc1.append(drawer.draw_arc(self.location.anchor_xy, p[0], p[1]))
            seg1.append(drawer.draw_line(p[1], p[2]))
            arc2.append(drawer.draw_arc(p[7], p[3], p[2]))
            arc3.append(drawer.draw_arc(p[7], p[4], p[3]))
            seg2.append(drawer.draw_line(p[4], p[5]))
            arc4.append(drawer.draw_arc(self.location.anchor_xy, p[5], p[6]))

        arc5.append(drawer.draw_arc(self.location.anchor_xy,
            [r_ri, DimMillimeter(0)], [- r_ri, DimMillimeter(0)]))
        arc6.append(drawer.draw_arc(self.location.anchor_xy,
            [- r_ri, DimMillimeter(0)], [r_ri, DimMillimeter(0)]))

        rad = (r_ri + x4) / 2
        inner_coord = self.location.transform_coords([[rad, 0]])
        segments = [arc1, seg1, arc2, arc3, seg2, arc4, arc5, arc6]
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

        if isinstance(self._dim_r_rb, DimLinear):
            pass
        else:
            raise TypeError("dim_r_rb not of type DimLinear")

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

class CrossSectInnerRotorRoundSlotsPartial(CrossSectBase):

    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for CrossSectInnerRotorRoundSlotsPartial class. This function takes in
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
    def dim_r_rb(self):
        return self._dim_r_rb

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
        r_rb = self.dim_r_rb
        d_so = self.dim_d_so
        w_so = self.dim_w_so
        Qr = self.Qr

        alpha_u = DimRadian(2 * np.pi / Qr)
        r1 = r_ri + d_ri + r_rb + DimMillimeter(np.sqrt(r_rb ** 2 - (w_so / 2) ** 2)) + d_so
        r2 = w_so / 2
        r_ro = DimMillimeter(np.sqrt(r1 ** 2 + r2 ** 2))

        x1 = r_ro * np.cos(alpha_u / 2)
        y1 = - r_ro * np.sin(alpha_u / 2)

        x2 = DimMillimeter(np.sqrt(r_ro ** 2 - (w_so / 2) ** 2))
        y2 = - w_so / 2

        x3 = x2 - d_so
        y3 = y2

        x4 = r_ri + d_ri
        y4 = DimMillimeter(0)

        x5 = x3
        y5 = - y3

        x6 = x2
        y6 = - y2

        x7 = x1
        y7 = - y1

        center_rotor_bar = [(x4 + r_rb), DimMillimeter(0)]

        x_arr = [x1, x2, x3, x4, x5, x6, x7, center_rotor_bar[0]]
        y_arr = [y1, y2, y3, y4, y5, y6, y7, center_rotor_bar[1]]

        arc1 = []
        arc2 = []
        arc3 = []
        arc4 = []
        arc5 = []
        seg1 = []
        seg2 = []
        seg3 = []
        seg4 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(0, 1):
            p = self.location.transform_coords(coords, alpha_u * i)

            arc1.append(drawer.draw_arc(self.location.anchor_xy, p[0], p[1]))
            seg1.append(drawer.draw_line(p[1], p[2]))
            arc2.append(drawer.draw_arc(p[7], p[3], p[2]))
            arc3.append(drawer.draw_arc(p[7], p[4], p[3]))
            seg2.append(drawer.draw_line(p[4], p[5]))
            arc4.append(drawer.draw_arc(self.location.anchor_xy, p[5], p[6]))

        x8 = r_ri * np.cos(alpha_u / 2)
        y8 = - r_ri * np.sin(alpha_u / 2)
        x9 = x8
        y9 = - y8
        arc5.append(drawer.draw_arc(self.location.anchor_xy,
            [x8, y8], [x9, y9]))
        seg3.append(drawer.draw_line(p[0], [x8, y8]))
        seg4.append(drawer.draw_line(p[6], [x9, y9]))

        rad = (r_ri + x4) / 2
        inner_coord = self.location.transform_coords([[rad, 0]])
        segments = [arc1, seg1, arc2, arc3, seg2, arc4, arc5, seg3, seg4]
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

        if isinstance(self._dim_r_rb, DimLinear):
            pass
        else:
            raise TypeError("dim_r_rb not of type DimLinear")

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

class CrossSectInnerRotorRoundSlotsBar(CrossSectBase):

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
        r_rb = self.rotor_core.dim_r_rb
        d_so = self.rotor_core.dim_d_so
        w_so = self.rotor_core.dim_w_so
        Qr = self.rotor_core.Qr

        alpha_u = DimRadian(2 * np.pi / Qr)
        r_b = r_ri + d_ri + r_rb

        x1 = r_b + r_rb
        y1 = DimMillimeter(0)

        x2 = r_b - r_rb
        y2 = DimMillimeter(0)

        center_rotor_bar = [r_b, DimMillimeter(0)]

        x_arr = [x1, x2, center_rotor_bar[0]]
        y_arr = [y1, y2, center_rotor_bar[1]]

        arc1 = []
        arc2 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        p = self.location.transform_coords(coords, 0)

        arc1.append(drawer.draw_arc(p[2], p[0], p[1]))
        arc1.append(drawer.draw_arc(p[2], p[1], p[0]))

        inner_coord = self.location.transform_coords([center_rotor_bar])
        segments = [arc1, arc2]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)

        return cs_token

    def _validate_attr(self):

        if (isinstance(self.rotor_core, CrossSectInnerRotorRoundSlots)) or (isinstance(self.rotor_core, CrossSectInnerRotorRoundSlotsPartial)):
            pass
        else:
            raise TypeError("rotor_core not of type CrossSectInnerRotorRoundSlots")