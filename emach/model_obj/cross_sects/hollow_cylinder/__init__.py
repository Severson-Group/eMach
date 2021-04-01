
import numpy as np

from ...dimensions.dim_linear import DimLinear
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectHollowCylinder']
class CrossSectHollowCylinder(CrossSectBase):
    
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
    def dim_t(self):
        return self._dim_t
    
    @property
    def dim_r_o(self):
        return self._dim_r_o
    
        
    
    def draw(self, drawer):

        r = self._dim_r_o # outer radius of hollow cylinder
        t = self._dim_t # thickness of hollow cylinder
    
        x_out = type(r)(0) # assign intial origin as DimLinear object of 0
        x_in = type(r)(0)
        x = [x_out, x_out, x_in, x_in]
        
        y_out = r
        y_in = r-t
        y = [-y_out, y_out, -y_in, y_in]
        z = np.array([x, y])
        
        coords = np.transpose(z)# convert coordinates to a form of [[x1,y1]..]
        
        p = self.location.transform_coords(coords) # shift coordinates based on anchor and theta given in location
        
        # draw hollow cylinder
        arc_out1 = drawer.draw_arc(self.location.anchor_xy, p[0,:], p[1,:])
        arc_out2 = drawer.draw_arc(self.location.anchor_xy, p[1,:], p[0,:])
        arc_out3 = drawer.draw_arc(self.location.anchor_xy, p[2,:], p[3,:])
        arc_out4 = drawer.draw_arc(self.location.anchor_xy, p[3,:], p[2,:])
        
        # get coordinate within hollow cylinder
        rad = r - t*0.5 
        inner_coord = self.location.transform_coords(np.array([[rad, type(r)(0)]]))
        
        token = [arc_out1, arc_out2, arc_out3, arc_out4] # compile tokens
        
        cs_token = CrossSectToken(inner_coord[0,:], token) # create CrossSectToken object
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
