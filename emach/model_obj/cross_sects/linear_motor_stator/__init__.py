import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimDegree
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectLinearMotorStator']


class CrossSectLinearMotorStator(CrossSectBase):
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
        # self._validate_attr()

    @property
    def dim_w_s(self):
        return self._dim_w_s

    @property
    def dim_w_st(self):
        return self._dim_w_st

    @property
    def dim_w_so(self):
        return self._dim_w_so

    @property
    def dim_r_so(self):
        return self._dim_r_so
    
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
    def dim_d_sy(self):
        return self._dim_d_sy
    
    @property
    def dim_r_st(self):
        return self._dim_r_st
    
    @property
    def dim_r_sf(self):
        return self._dim_r_sf
    
    @property
    def dim_r_sb(self):
        return self._dim_r_sb
    
    def draw(self, drawer):
        # linear motor stator parameters
        w_s = self.dim_w_s
        w_st = self.dim_w_st
        w_so = self.dim_w_so
        r_so = self.dim_r_so
        r_si = self.dim_r_si
        d_so = self.dim_d_so
        d_sp = self.dim_d_sp
        d_sy = self.dim_d_sy
        r_st = self.dim_r_st       
        r_sf = self.dim_r_sf
        r_sb = self.dim_r_sb 
        
        # x-axis coordinates of stator points
        x1 = r_si
        x2 = r_si + d_so
        x3 = r_si + d_sp
        x4 = r_so - d_sy
        x5 = r_so
        
        # y-axis coordinates of stator points
        y1 = 0
        y2 = w_st/2
        y3 = (w_s-w_so*2)/4
        y4 = y3+w_so
        y5 = y4+y3-y2
        y6 = y5+w_st
        y7 = y6+y3-y2
        y8 = y7+w_so
        y9 = y8+y3-y2
        y10 = y9+w_st/2
            
        # build x and y coordinates of stator points as arrays based on
        # the order how these points are connected between each other
        x = [ x1, x5, x5,  x1,  x1, x2, x3, x4, x4, x3, x2, x1, \
              x1, x2, x3, x4, x4, x3, x2, x1];
        y = [ y1, y1, y10, y10, y8, y8, y9, y9, y6, y6, y7, y7, \
              y4, y4, y5, y5, y2, y2, y3, y3];
        
        p = np.array([x, y])

        p = np.transpose(p)

        points = self.location.transform_coords(p)

        seg1 = drawer.draw_line(points[0, :], points[1, :])
        seg2 = drawer.draw_line(points[1, :], points[2, :])
        seg3 = drawer.draw_line(points[2, :], points[3, :])
        seg4 = drawer.draw_line(points[3, :], points[4, :])
        seg5 = drawer.draw_line(points[4, :], points[5, :])
        seg6 = drawer.draw_line(points[5, :], points[6, :])
        seg7 = drawer.draw_line(points[6, :], points[7, :])
        seg8 = drawer.draw_line(points[7, :], points[8, :])
        seg9 = drawer.draw_line(points[8, :], points[9, :])
        seg10 = drawer.draw_line(points[9, :], points[10, :])
        seg11 = drawer.draw_line(points[10, :], points[11, :])
        seg12 = drawer.draw_line(points[11, :], points[12, :])
        seg13 = drawer.draw_line(points[12, :], points[13, :])
        seg14 = drawer.draw_line(points[13, :], points[14, :])
        seg15 = drawer.draw_line(points[14, :], points[15, :])
        seg16 = drawer.draw_line(points[15, :], points[16, :])
        seg17 = drawer.draw_line(points[16, :], points[17, :])
        seg18 = drawer.draw_line(points[17, :], points[18, :])
        seg19 = drawer.draw_line(points[18, :], points[19, :])
        seg20 = drawer.draw_line(points[19, :], points[0, :])
        
        x_coord = x3
        y_coord = (y5 + y6)/2
        inner_coord = self.location.transform_coords(np.array([[x_coord, y_coord]]))

        segments = [seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, \
                seg9, seg10, seg11, seg12, seg13, seg14, seg15, seg16, \
                seg17, seg18, seg19, seg20]

        cs_token = CrossSectToken(inner_coord[0, :], segments)  # create CrossSectToken selfect

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



