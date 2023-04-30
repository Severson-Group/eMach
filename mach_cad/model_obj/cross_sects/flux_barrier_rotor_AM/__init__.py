import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectFluxBarrierRotorAMPartial_Iron1','CrossSectFluxBarrierRotorAMPartial_Iron2','CrossSectFluxBarrierRotorAMPartial_Iron3','CrossSectFluxBarrierRotorAMPartial_Barrier1','CrossSectFluxBarrierRotorAMPartial_Barrier2']

class CrossSectFluxBarrierRotorAMPartial_Iron1(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Flux Barrier Rotor class. This function takes in
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
    def dim_r_ri(self):
        return self._dim_r_ri

    @property
    def dim_r_ro(self):
        return self._dim_r_ro

    @property
    def dim_d_r1(self):
        return self._dim_d_r1

    @property
    def dim_d_r2(self):
        return self._dim_d_r2

    @property
    def dim_w_b1(self):
        return self._dim_w_b1

    @property
    def dim_w_b2(self):
        return self._dim_w_b2
    
    @property
    def p(self):
        return self._p

    def draw(self, drawer):
        r_ri = self.dim_r_ri
        r_ro = self.dim_r_ro
        d_r1 = self.dim_d_r1
        d_r2 = self.dim_d_r2
        w_b1 = self.dim_w_b1
        w_b2 = self.dim_w_b2
        p = self.p

        # First Magnetic Segment

        # Point on Shaft
        x0 = 0
        y0 = r_ri
        x1 = r_ri
        y1 = 0
        # Mid Point in Rotor
        x2 = (r_ri + d_r1) * np.cos(np.pi / (2 * p))
        y2 = (r_ri + d_r1) * np.sin(np.pi / (2 * p))
        # Corner Points on Rotor Surface
        x3 = 0
        y3 = r_ro
        x6 = r_ro
        y6 = 0
        # Points on Rotor Surface
        x4 = x2
        y4 = np.sqrt(r_ro**2 - x2**2)
        x5 = np.sqrt(r_ro**2 - y2**2)
        y5 = y2

        # First Barrier Segment

        # Mid Point in Rotor
        x7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x8 = x7
        y8 = np.sqrt(r_ro**2 - x7**2)
        x9 = np.sqrt(r_ro**2 - y7**2)
        y9 = y7

        # Second Magnetic Segment

        # Mid Point in Rotor
        x10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.cos(np.pi / (2 * p))
        y10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x11 = x10
        y11 = np.sqrt(r_ro**2 - x10**2)
        x12 = np.sqrt(r_ro**2 - y10**2)
        y12 = y10

        # Second Barrier Segment

        # Mid Point in Rotor
        x13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x14 = x13
        y14 = np.sqrt(r_ro**2 - x13**2)
        x15 = np.sqrt(r_ro**2 - y13**2)
        y15 = y13

        x_arr = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15]
        y_arr = [y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15]

        # Shaft
        arc1 = []
        # Magnetic Section 1
        seg1 = []
        arc2 = []
        seg2 = []
        seg3 = []
        arc3 = []
        seg4 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(0, 1):
            po = self.location.transform_coords(coords, (np.pi / 2)* i)
            
            # Shaft
            arc1.append(drawer.draw_arc(self.location.anchor_xy, po[1], po[0]))
            
            # Magnetic Section 1
            seg1.append(drawer.draw_line(po[0], po[3]))
            arc2.append(drawer.draw_arc(self.location.anchor_xy, po[4], po[3]))
            seg2.append(drawer.draw_line(po[4], po[2]))
            seg3.append(drawer.draw_line(po[2],po[5]))
            arc3.append(drawer.draw_arc(self.location.anchor_xy, po[6], po[5]))
            seg4.append(drawer.draw_line(po[6],po[1]))
                        
        rad = (r_ri + d_r1/2) # <---- SOURCE OF ERROR?
        inner_coord = self.location.transform_coords([[rad*np.cos(np.pi/(2*p)),rad*np.sin(np.pi/(2*p))]])
        segments = [arc1,seg1,arc2,seg2,seg3,arc3,seg4]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_r_ri, DimLinear):
            raise TypeError('dim_r_ri is not of DimLinear')

        if not isinstance(self._dim_r_ro, DimLinear):
            raise TypeError('dim_r_ro is not of DimLinear')

        if not isinstance(self._dim_d_r1, DimLinear):
            raise TypeError('dim_d_r1 is not of DimLinear')

        if not isinstance(self._dim_d_r2, DimLinear):
            raise TypeError('dim_d_r2 is not of DimLinear')

        if not isinstance(self._dim_w_b1, DimLinear):
            raise TypeError('dim_w_b1 is not of DimLinear')

        if not isinstance(self._dim_w_b2, DimLinear):
            raise TypeError('dim_w_b2 is not of DimLinear')

        if not isinstance(self._p, int):
            raise TypeError('p is not of int')
        

class CrossSectFluxBarrierRotorAMPartial_Iron2(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Flux Barrier Rotor class. This function takes in
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
    def dim_r_ri(self):
        return self._dim_r_ri

    @property
    def dim_r_ro(self):
        return self._dim_r_ro

    @property
    def dim_d_r1(self):
        return self._dim_d_r1

    @property
    def dim_d_r2(self):
        return self._dim_d_r2

    @property
    def dim_w_b1(self):
        return self._dim_w_b1

    @property
    def dim_w_b2(self):
        return self._dim_w_b2
    
    @property
    def p(self):
        return self._p

    def draw(self, drawer):
        r_ri = self.dim_r_ri
        r_ro = self.dim_r_ro
        d_r1 = self.dim_d_r1
        d_r2 = self.dim_d_r2
        w_b1 = self.dim_w_b1
        w_b2 = self.dim_w_b2
        p = self.p

        # First Magnetic Segment

        # Point on Shaft
        x0 = 0
        y0 = r_ri
        x1 = r_ri
        y1 = 0
        # Mid Point in Rotor
        x2 = (r_ri + d_r1) * np.cos(np.pi / (2 * p))
        y2 = (r_ri + d_r1) * np.sin(np.pi / (2 * p))
        # Corner Points on Rotor Surface
        x3 = 0
        y3 = r_ro
        x6 = r_ro
        y6 = 0
        # Points on Rotor Surface
        x4 = x2
        y4 = np.sqrt(r_ro**2 - x2**2)
        x5 = np.sqrt(r_ro**2 - y2**2)
        y5 = y2

        # First Barrier Segment

        # Mid Point in Rotor
        x7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x8 = x7
        y8 = np.sqrt(r_ro**2 - x7**2)
        x9 = np.sqrt(r_ro**2 - y7**2)
        y9 = y7

        # Second Magnetic Segment

        # Mid Point in Rotor
        x10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.cos(np.pi / (2 * p))
        y10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x11 = x10
        y11 = np.sqrt(r_ro**2 - x10**2)
        x12 = np.sqrt(r_ro**2 - y10**2)
        y12 = y10

        # Second Barrier Segment

        # Mid Point in Rotor
        x13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x14 = x13
        y14 = np.sqrt(r_ro**2 - x13**2)
        x15 = np.sqrt(r_ro**2 - y13**2)
        y15 = y13

        x_arr = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15]
        y_arr = [y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15]

        # Magnetic Section 2
        seg9 = []
        arc6 = []
        seg10 = []
        seg11 = []
        arc7 = []
        seg12 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(0, 1):
            po = self.location.transform_coords(coords, (np.pi / 2)* i)

            # Magnetic Section 2
            seg9.append(drawer.draw_line(po[7], po[8]))
            arc6.append(drawer.draw_arc(self.location.anchor_xy, po[11], po[8]))
            seg10.append(drawer.draw_line(po[11], po[10]))
            seg11.append(drawer.draw_line(po[10],po[12]))
            arc7.append(drawer.draw_arc(self.location.anchor_xy, po[9], po[12]))
            seg12.append(drawer.draw_line(po[9],po[7]))
                        
        rad = (r_ri + d_r1 + w_b1 / np.cos(np.pi / (2 * p)) + d_r2/2) # <---- SOURCE OF ERROR?
        inner_coord = self.location.transform_coords([[rad*np.cos(np.pi/(2*p)),rad*np.sin(np.pi/(2*p))]])
        segments = [seg9,arc6,seg10,seg11,arc7,seg12]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_r_ri, DimLinear):
            raise TypeError('dim_r_ri is not of DimLinear')

        if not isinstance(self._dim_r_ro, DimLinear):
            raise TypeError('dim_r_ro is not of DimLinear')

        if not isinstance(self._dim_d_r1, DimLinear):
            raise TypeError('dim_d_r1 is not of DimLinear')

        if not isinstance(self._dim_d_r2, DimLinear):
            raise TypeError('dim_d_r2 is not of DimLinear')

        if not isinstance(self._dim_w_b1, DimLinear):
            raise TypeError('dim_w_b1 is not of DimLinear')

        if not isinstance(self._dim_w_b2, DimLinear):
            raise TypeError('dim_w_b2 is not of DimLinear')

        if not isinstance(self._p, int):
            raise TypeError('p is not of int')
        

class CrossSectFluxBarrierRotorAMPartial_Iron3(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Flux Barrier Rotor class. This function takes in
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
    def dim_r_ri(self):
        return self._dim_r_ri

    @property
    def dim_r_ro(self):
        return self._dim_r_ro

    @property
    def dim_d_r1(self):
        return self._dim_d_r1

    @property
    def dim_d_r2(self):
        return self._dim_d_r2

    @property
    def dim_w_b1(self):
        return self._dim_w_b1

    @property
    def dim_w_b2(self):
        return self._dim_w_b2
    
    @property
    def p(self):
        return self._p

    def draw(self, drawer):
        r_ri = self.dim_r_ri
        r_ro = self.dim_r_ro
        d_r1 = self.dim_d_r1
        d_r2 = self.dim_d_r2
        w_b1 = self.dim_w_b1
        w_b2 = self.dim_w_b2
        p = self.p

        # First Magnetic Segment

        # Point on Shaft
        x0 = 0
        y0 = r_ri
        x1 = r_ri
        y1 = 0
        # Mid Point in Rotor
        x2 = (r_ri + d_r1) * np.cos(np.pi / (2 * p))
        y2 = (r_ri + d_r1) * np.sin(np.pi / (2 * p))
        # Corner Points on Rotor Surface
        x3 = 0
        y3 = r_ro
        x6 = r_ro
        y6 = 0
        # Points on Rotor Surface
        x4 = x2
        y4 = np.sqrt(r_ro**2 - x2**2)
        x5 = np.sqrt(r_ro**2 - y2**2)
        y5 = y2

        # First Barrier Segment

        # Mid Point in Rotor
        x7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x8 = x7
        y8 = np.sqrt(r_ro**2 - x7**2)
        x9 = np.sqrt(r_ro**2 - y7**2)
        y9 = y7

        # Second Magnetic Segment

        # Mid Point in Rotor
        x10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.cos(np.pi / (2 * p))
        y10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x11 = x10
        y11 = np.sqrt(r_ro**2 - x10**2)
        x12 = np.sqrt(r_ro**2 - y10**2)
        y12 = y10

        # Second Barrier Segment

        # Mid Point in Rotor
        x13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x14 = x13
        y14 = np.sqrt(r_ro**2 - x13**2)
        x15 = np.sqrt(r_ro**2 - y13**2)
        y15 = y13

        x_arr = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15]
        y_arr = [y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15]

        # Third Magnetic Arc
        seg17 = []
        arc10 = []
        seg18 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(0, 1):
            po = self.location.transform_coords(coords, (np.pi / 2)* i)

            # Third Magnetic Arc
            seg17.append(drawer.draw_line(po[13], po[14]))
            arc10.append(drawer.draw_arc(self.location.anchor_xy, po[15], po[14]))
            seg18.append(drawer.draw_line(po[15], po[13]))
                        
        rad = r_ro
        inner_coord = self.location.transform_coords([[rad*np.cos(np.pi/(2*p)),rad*np.sin(np.pi/(2*p))]])
        segments = [seg17,arc10,seg18]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_r_ri, DimLinear):
            raise TypeError('dim_r_ri is not of DimLinear')

        if not isinstance(self._dim_r_ro, DimLinear):
            raise TypeError('dim_r_ro is not of DimLinear')

        if not isinstance(self._dim_d_r1, DimLinear):
            raise TypeError('dim_d_r1 is not of DimLinear')

        if not isinstance(self._dim_d_r2, DimLinear):
            raise TypeError('dim_d_r2 is not of DimLinear')

        if not isinstance(self._dim_w_b1, DimLinear):
            raise TypeError('dim_w_b1 is not of DimLinear')

        if not isinstance(self._dim_w_b2, DimLinear):
            raise TypeError('dim_w_b2 is not of DimLinear')

        if not isinstance(self._p, int):
            raise TypeError('p is not of int')
        

class CrossSectFluxBarrierRotorAMPartial_Barrier1(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Flux Barrier Rotor class. This function takes in
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
    def dim_r_ri(self):
        return self._dim_r_ri

    @property
    def dim_r_ro(self):
        return self._dim_r_ro

    @property
    def dim_d_r1(self):
        return self._dim_d_r1

    @property
    def dim_d_r2(self):
        return self._dim_d_r2

    @property
    def dim_w_b1(self):
        return self._dim_w_b1

    @property
    def dim_w_b2(self):
        return self._dim_w_b2
    
    @property
    def p(self):
        return self._p

    def draw(self, drawer):
        r_ri = self.dim_r_ri
        r_ro = self.dim_r_ro
        d_r1 = self.dim_d_r1
        d_r2 = self.dim_d_r2
        w_b1 = self.dim_w_b1
        w_b2 = self.dim_w_b2
        p = self.p

        # First Magnetic Segment

        # Point on Shaft
        x0 = 0
        y0 = r_ri
        x1 = r_ri
        y1 = 0
        # Mid Point in Rotor
        x2 = (r_ri + d_r1) * np.cos(np.pi / (2 * p))
        y2 = (r_ri + d_r1) * np.sin(np.pi / (2 * p))
        # Corner Points on Rotor Surface
        x3 = 0
        y3 = r_ro
        x6 = r_ro
        y6 = 0
        # Points on Rotor Surface
        x4 = x2
        y4 = np.sqrt(r_ro**2 - x2**2)
        x5 = np.sqrt(r_ro**2 - y2**2)
        y5 = y2

        # First Barrier Segment

        # Mid Point in Rotor
        x7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x8 = x7
        y8 = np.sqrt(r_ro**2 - x7**2)
        x9 = np.sqrt(r_ro**2 - y7**2)
        y9 = y7

        # Second Magnetic Segment

        # Mid Point in Rotor
        x10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.cos(np.pi / (2 * p))
        y10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x11 = x10
        y11 = np.sqrt(r_ro**2 - x10**2)
        x12 = np.sqrt(r_ro**2 - y10**2)
        y12 = y10

        # Second Barrier Segment

        # Mid Point in Rotor
        x13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x14 = x13
        y14 = np.sqrt(r_ro**2 - x13**2)
        x15 = np.sqrt(r_ro**2 - y13**2)
        y15 = y13

        x_arr = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15]
        y_arr = [y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15]

        # Barrier Section 1
        seg5 = []
        arc4 = []
        seg6 = []
        seg7 = []
        arc5 = []
        seg8 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(0, 1):
            po = self.location.transform_coords(coords, (np.pi / 2)* i)

            # Barrier Section 1
            seg5.append(drawer.draw_line(po[2], po[4]))
            arc4.append(drawer.draw_arc(self.location.anchor_xy, po[8], po[4]))
            seg6.append(drawer.draw_line(po[8], po[7]))
            seg7.append(drawer.draw_line(po[7],po[9]))
            arc5.append(drawer.draw_arc(self.location.anchor_xy, po[5], po[9]))
            seg8.append(drawer.draw_line(po[5],po[2]))

                        
        rad = (r_ri + d_r1 + (w_b1 / np.cos(np.pi / (2 * p)))/2)
        inner_coord = self.location.transform_coords([[rad*np.cos(np.pi/(2*p)),rad*np.sin(np.pi/(2*p))]])
        segments = [seg5,arc4,seg6,seg7,arc5,seg8]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_r_ri, DimLinear):
            raise TypeError('dim_r_ri is not of DimLinear')

        if not isinstance(self._dim_r_ro, DimLinear):
            raise TypeError('dim_r_ro is not of DimLinear')

        if not isinstance(self._dim_d_r1, DimLinear):
            raise TypeError('dim_d_r1 is not of DimLinear')

        if not isinstance(self._dim_d_r2, DimLinear):
            raise TypeError('dim_d_r2 is not of DimLinear')

        if not isinstance(self._dim_w_b1, DimLinear):
            raise TypeError('dim_w_b1 is not of DimLinear')

        if not isinstance(self._dim_w_b2, DimLinear):
            raise TypeError('dim_w_b2 is not of DimLinear')

        if not isinstance(self._p, int):
            raise TypeError('p is not of int')
        

class CrossSectFluxBarrierRotorAMPartial_Barrier2(CrossSectBase):
    def __init__(self, **kwargs: any) -> None:
        '''
        Initialization function for Flux Barrier Rotor class. This function takes in
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
    def dim_r_ri(self):
        return self._dim_r_ri

    @property
    def dim_r_ro(self):
        return self._dim_r_ro

    @property
    def dim_d_r1(self):
        return self._dim_d_r1

    @property
    def dim_d_r2(self):
        return self._dim_d_r2

    @property
    def dim_w_b1(self):
        return self._dim_w_b1

    @property
    def dim_w_b2(self):
        return self._dim_w_b2
    
    @property
    def p(self):
        return self._p

    def draw(self, drawer):
        r_ri = self.dim_r_ri
        r_ro = self.dim_r_ro
        d_r1 = self.dim_d_r1
        d_r2 = self.dim_d_r2
        w_b1 = self.dim_w_b1
        w_b2 = self.dim_w_b2
        p = self.p

        # First Magnetic Segment

        # Point on Shaft
        x0 = 0
        y0 = r_ri
        x1 = r_ri
        y1 = 0
        # Mid Point in Rotor
        x2 = (r_ri + d_r1) * np.cos(np.pi / (2 * p))
        y2 = (r_ri + d_r1) * np.sin(np.pi / (2 * p))
        # Corner Points on Rotor Surface
        x3 = 0
        y3 = r_ro
        x6 = r_ro
        y6 = 0
        # Points on Rotor Surface
        x4 = x2
        y4 = np.sqrt(r_ro**2 - x2**2)
        x5 = np.sqrt(r_ro**2 - y2**2)
        y5 = y2

        # First Barrier Segment

        # Mid Point in Rotor
        x7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y7 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x8 = x7
        y8 = np.sqrt(r_ro**2 - x7**2)
        x9 = np.sqrt(r_ro**2 - y7**2)
        y9 = y7

        # Second Magnetic Segment

        # Mid Point in Rotor
        x10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.cos(np.pi / (2 * p))
        y10 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x11 = x10
        y11 = np.sqrt(r_ro**2 - x10**2)
        x12 = np.sqrt(r_ro**2 - y10**2)
        y12 = y10

        # Second Barrier Segment

        # Mid Point in Rotor
        x13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.cos(np.pi / (2 * p))
        y13 = (r_ri + d_r1 + w_b1/np.sin(np.pi / (2 * p)) + d_r2 + w_b2/np.sin(np.pi / (2 * p))) * np.sin(np.pi / (2 * p))
        # Points on Rotor Surface
        x14 = x13
        y14 = np.sqrt(r_ro**2 - x13**2)
        x15 = np.sqrt(r_ro**2 - y13**2)
        y15 = y13

        x_arr = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15]
        y_arr = [y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15]

        #Barrier Section 2
        seg13 = []
        arc8 = []
        seg14 = []
        seg15 = []
        arc9 = []
        seg16 = []

        # transpose list
        coords = [x_arr, y_arr]
        coords = list(zip(*coords))
        coords = [list(sublist) for sublist in coords]

        for i in range(0, 1):
            po = self.location.transform_coords(coords, (np.pi / 2)* i)

            # Barrier Section 2
            seg13.append(drawer.draw_line(po[10], po[11]))
            arc8.append(drawer.draw_arc(self.location.anchor_xy, po[14], po[11]))
            seg14.append(drawer.draw_line(po[14], po[13]))
            seg15.append(drawer.draw_line(po[13],po[15]))
            arc9.append(drawer.draw_arc(self.location.anchor_xy, po[12], po[15]))
            seg16.append(drawer.draw_line(po[12],po[10]))
                        
        rad = (r_ri + d_r1 + w_b1 / np.cos(np.pi / (2 * p)) + d_r2 + (w_b2 / np.cos(np.pi / (2 * p)))/2)
        inner_coord = self.location.transform_coords([[rad*np.cos(np.pi/(2*p)),rad*np.sin(np.pi/(2*p))]])
        segments = [seg13,arc8,seg14,seg15,arc9,seg16]
        segs = [x for segment in segments for x in segment]
        cs_token = CrossSectToken(inner_coord[0], segs)  # create CrossSectToken object
        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_r_ri, DimLinear):
            raise TypeError('dim_r_ri is not of DimLinear')

        if not isinstance(self._dim_r_ro, DimLinear):
            raise TypeError('dim_r_ro is not of DimLinear')

        if not isinstance(self._dim_d_r1, DimLinear):
            raise TypeError('dim_d_r1 is not of DimLinear')

        if not isinstance(self._dim_d_r2, DimLinear):
            raise TypeError('dim_d_r2 is not of DimLinear')

        if not isinstance(self._dim_w_b1, DimLinear):
            raise TypeError('dim_w_b1 is not of DimLinear')

        if not isinstance(self._dim_w_b2, DimLinear):
            raise TypeError('dim_w_b2 is not of DimLinear')

        if not isinstance(self._p, int):
            raise TypeError('p is not of int')