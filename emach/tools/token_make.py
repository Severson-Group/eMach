

class TokenMake:
    
    def __init__(self, cs_token = [], prep_sect_token = [], make_solid_token = []):
        self._cs_token = cs_token
        self._prep_sect_token = prep_sect_token
        self._make_solid_token = make_solid_token
    
    @property
    def cs_token(self):
        return self._cs_token
    
    @property
    def prep_sect_token(self):
        return self._prep_sect_token
    
    @property
    def make_solid_token(self):
        return self._make_solid_token