import numpy as np

from ...dimensions.dim_linear import DimLinear
from ...dimensions.dim_angular import DimAngular
from ...dimensions import DimRadian
from ..cross_sect_base import CrossSectBase, CrossSectToken

__all__ = ['CrossSectBreadloaf']


class CrossSectBreadloaf(CrossSectBase):

    def __init__(self, **kwargs: any) -> None:
        '''
        Intialization function for CrossSectBreadloaf class. This function takes in
        arguments and saves the information passed to private variable to make
        them read-only
        Parameters
        ----------
        **kwargs : any
            DESCRIPTION. Keyword arguments provided to the initialization funcntion.
            The following argument names have to be included in order for the code
            to execute: name, dim_w, dim_l, dim_r, dim_alpha, location. 
            
        Returns
        -------
        None
        '''
        self._create_attr(kwargs)

        super()._validate_attr()
        self._validate_attr()

    @property
    def dim_w(self):
        return self._dim_w

    @property
    def dim_l(self):
        return self._dim_l

    @property
    def dim_r(self):
        return self._dim_r

    @property
    def dim_alpha(self):
        return self._dim_alpha

    def draw(self, drawer):

        w = self._dim_w
        l = self._dim_l
        r = self._dim_r
        alpha = DimRadian(self._dim_alpha)

        y_in = type(r)(0)
        p1 = [w / 2, y_in]
        p2 = [w / 2 - l * np.cos(alpha), l * np.sin(alpha)]
        p3 = [-w / 2 + l * np.cos(alpha), l * np.sin(alpha)]
        p4 = [-w / 2, y_in]

        beta = np.arcsin(p2[0] / r)
        base = r * np.cos(beta)
        arc_center = [y_in, -(base - p2[1])]

        # transform coords
        p1 = self.location.transform_coords([p1])
        p2 = self.location.transform_coords([p2])
        p3 = self.location.transform_coords([p3])
        p4 = self.location.transform_coords([p4])
        arcCenter = self.location.transform_coords([arc_center])

        # Draw segments
        rightSeg = drawer.draw_line(p1[0], p2[0])
        arc = drawer.draw_arc(arcCenter[0], p2[0], p3[0])
        leftSeg = drawer.draw_line(p3[0], p4[0])
        baseSeg = drawer.draw_line(p4[0], p1[0])

        # get coordinate within breadloaf
        ic = [y_in, l * np.sin(alpha) / 2]
        inner_coord = self.location.transform_coords([ic])

        segments = [rightSeg, arc, leftSeg, baseSeg]

        cs_token = CrossSectToken(inner_coord[0], segments)

        return cs_token

    def _validate_attr(self):

        if not isinstance(self._dim_w, DimLinear):
            raise TypeError("dim_w not of type DimLinear")

        if not isinstance(self._dim_l, DimLinear):
            raise TypeError("dim_l not of type DimLinear")

        if not isinstance(self._dim_r, DimLinear):
            raise TypeError("dim_r not of type DimLinear")

        if not isinstance(self._dim_alpha, DimAngular):
            raise TypeError("dim_r not of type DimAngular")
