from .make_solid_base import MakeSolidBase
from ...tools.token_make import TokenMake
from ..dimensions.dim_linear import DimLinear

__all__ = ['MakeExtrude']


class MakeExtrude(MakeSolidBase):

    def __init__(self, **kwargs: any) -> None:
        self._create_attr(kwargs)

        super()._validate_attr()
        self._validate_attr()

    @property
    def dim_depth(self):
        return self._dim_depth

    def _validate_attr(self):
        if not isinstance(self._dim_depth, DimLinear):
            raise TypeError("Expected input to be one of the following type: \
                             DimLinear. Instead it was of type " + \
                            str(type(self._dim_depth)))

    def run(self, name, material, cs_token, maker):
        token1 = []
        for i in range(len(cs_token)):
            token1.append(maker.prepare_section(cs_token[i]))

        token2 = maker.extrude(name, material, self._dim_depth, token1)

        token_make = TokenMake(cs_token, token1, token2)
        return token_make
