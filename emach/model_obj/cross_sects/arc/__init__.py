
import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectArc']
class CrossSectArc(CrossSectBase):
    
    def __init__(self, **kwargs: any) -> None: 
        '''
        Intialization function for Arc class. This function takes in
        arguments and saves the information passed to private variable to make
        them read-only
        Parameters
        ----------
        **kwargs : any
            DESCRIPTION. Keyword arguments provided to the initialization funcntion.
            The following argument names have to be included in order for the code
            to execute: name, dim_d_a, dim_r_o, dim_alpha, location. 
            
        Returns
        -------
        None
        '''
        self._create_attr(kwargs)  
        
        super()._validate_attr()
        self._validate_attr()
    
    @property
    def dim_d_a(self):
        return self._dim_d_a
    
    @property
    def dim_r_o(self):
        return self._dim_r_o
    
    @property
    def dim_alpha(self):
        return self._dim_alpha
    
    
    def draw(self, drawer):

        r = self._dim_r_o # outer radius of arc
        t = self._dim_d_a # thickness of arc
        alpha = DimRadian(self._dim_alpha)
        
        x_out = r*np.cos(alpha/2)
        x_in = (r-t)*np.cos(alpha/2)
        x = [x_out, x_out, x_in, x_in]

        y_out = r*np.sin(alpha/2);
        y_in = (r-t)*np.sin(alpha/2);
        y = [-y_out, y_out, y_in, -y_in];
        
        
        z = np.array([x, y])
        
        coords = np.transpose(z)# convert coordinates to a form of [[x1,y1]..]
        
        p = self.location.transform_coords(coords) # shift coordinates based on anchor and theta given in location
        
        # draw hollow cylinder
        arc_out = drawer.draw_arc(self.location.anchor_xy, p[0,:], p[1,:])
        line_cc = drawer.draw_line(p[1,:], p[2,:])
        arc_in = drawer.draw_arc(self.location.anchor_xy, p[3,:], p[2,:])
        line_cw = drawer.draw_line(p[3,:], p[0,:])
        
        # get coordinate within hollow cylinder
        rad = r - t*0.5 
        inner_coord = self.location.transform_coords(np.array([[rad, type(r)(0)]]))
        
        token = [arc_out, line_cc, arc_in, line_cw] # compile tokens
        
        cs_token = CrossSectToken(inner_coord[0,:], token) # create CrossSectToken object
        return cs_token
        
    def _validate_attr(self):
        
        if not isinstance(self._dim_r_o, DimLinear):
            raise TypeError("dim_r_o not of type DimLinear")
            
        if not isinstance(self._dim_d_a, DimLinear):
            raise TypeError("dim_d_a not of type DimLinear")     
            
        if not isinstance(self._dim_alpha, DimAngular):
            raise TypeError("dim_alpha not of type DimAngular")  
