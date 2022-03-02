import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectInnerReluctanceRotor']

class CrossSectInnerReluctanceRotor(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Inner Reluctance Rotor class. This function takes in
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
    def dim_alpha_rpi(self):
        return self._dim_alpha_rpi

    @property
    def dim_alpha_rpo(self):
        return self._dim_alpha_rpo

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
    def dim_r_if(self):
        return self._dim_r_if

    @property
    def dim_r_of(self):
        return self._dim_r_of

    @property
    def Q_r(self):
        return self._Q_r

    def draw(self, drawer):
        alpha_rpi = DimRadian(self.dim_alpha_rpi)
        alpha_rpo = DimRadian(self.dim_alpha_rpo)
        r_ri = self.dim_r_ri
        d_ri = self.dim_d_ri
        d_rp = self.dim_d_rp
        r_if = self.dim_r_if
        r_of = self.dim_r_of
        Q_r = self.Q_r

        alpha_total = DimRadian(2* np.pi / (Q_r))

        # Shaft
        x1 = r_ri * np.cos(alpha_total / 2)
        y1 = r_ri * np.sin(alpha_total / 2)
        
        # Outer wall arc(above tooth[below is mirror])
        x2 = (r_ri + d_ri) * np.cos(alpha_total / 2)  # top point
        y2 = (r_ri + d_ri) * np.sin(alpha_total / 2)  # top point

        # Centre of wall arc
        x9 = ((r_ri + d_ri) + (r_ri + d_ri))*np.cos(alpha_total / 4)
        y9 = ((r_ri + d_ri) + (r_ri + d_ri))*np.sin(alpha_total / 4)

        # Starting of Tooth (Upper Point of Fillet)
        x3 = (r_ri + d_ri) * np.cos((alpha_rpi / 2)+((alpha_rpi / 2)/10))  # top point
        y3 = (r_ri + d_ri) * np.sin((alpha_rpi / 2)+((alpha_rpi / 2)/10))  # top point
        
        # Centre of Inner Fillet
        x5 = x3 + (r_if)/(np.sqrt(2))
        y5 = y3

        # Starting of Tooth (Bottom Point of Fillet)
        x4 = x5
        y4 = y5 - (r_if)/(np.sqrt(2))

        # Outer Tooth arc Right Point of Fillet
        x7 = (r_ri + d_ri + d_rp) * np.cos((alpha_rpo / 2)-((alpha_rpo / 2)/10))
        y7 = (r_ri + d_ri + d_rp) * np.sin((alpha_rpo / 2)-((alpha_rpo / 2)/10))

        # Centre of Outer Fillet
        x8 = x7 - r_of
        y8 = y7

        # Outer Tooth arc Left Point of Fillet
        x6 = x8
        y6 = y8 + r_of
                           
        x_arr = [x1, x1, x2, x3, x4, x5, x6, x7, x8, x7, x6, x8, x4, x3, x5, x2, x9, x9]
        y_arr = [-y1, y1, y2, y3, y4, y5, y6, y7, y8, -y7, -y6, -y8, -y4, -y3, -y5, -y2, y9, -y9]

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

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(1, (Q_r +1)):
            po = self.location.transform_coords(coords, alpha_total * i)

            arc1.append(drawer.draw_arc(self.location.anchor_xy, po[0], po[1])) # Shaft
            arc2.append(drawer.draw_arc(self.location.anchor_xy, po[3], po[2])) # Rotor Core to fillet start (Top)
            arc3.append(drawer.draw_arc(po[5], po[3], po[4])) # Inner Fillet (Top)
            seg1.append(drawer.draw_line(po[6], po[4])) # Rotor Tooth (Top)
            arc4.append(drawer.draw_arc(po[8], po[7], po[6])) # Outer Fillet (Top)
            arc5.append(drawer.draw_arc(self.location.anchor_xy, po[9], po[7])) # Outer Rotor tooth arc
            arc6.append(drawer.draw_arc(po[11], po[10], po[9])) # Outer Fillet (Bottom)
            seg2.append(drawer.draw_line(po[10], po[12])) # Rotor Tooth (Bottom)
            arc7.append(drawer.draw_arc(po[14], po[12], po[13])) # Inner Fillet (Bottom)
            arc8.append(drawer.draw_arc(self.location.anchor_xy, po[15], po[13])) # Rotor Core to fillet start (Bottom)

        rad = (x1 + x7) / 2
        inner_coord = self.location.transform_coords([[rad, 0]])
        segments = [arc1, arc2, seg1, arc3, seg2, arc4, arc5, arc6, arc7, arc8]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_alpha_rpi, DimAngular):
            raise TypeError('dim_alpha_rpi is not of DimAngular')

        if not isinstance(self._dim_alpha_rpo, DimAngular):
            raise TypeError('dim_alpha_rpo is not of DimAngular')

        if not isinstance(self._dim_r_ri, DimLinear):
            raise TypeError('dim_r_ri is not of DimLinear')

        if not isinstance(self._dim_d_ri, DimLinear):
            raise TypeError('dim_d_ri is not of DimLinear')

        if not isinstance(self._dim_d_rp, DimLinear):
            raise TypeError('dim_d_rp is not of DimLinear')

        if not isinstance(self._dim_r_if, DimLinear):
            raise TypeError('dim_r_if is not of DimLinear')

        if not isinstance(self._dim_r_of, DimLinear):
            raise TypeError('dim_r_of is not of DimLinear')

        if not isinstance(self._Q_r, int):
            raise TypeError('Q_r is not of int')
