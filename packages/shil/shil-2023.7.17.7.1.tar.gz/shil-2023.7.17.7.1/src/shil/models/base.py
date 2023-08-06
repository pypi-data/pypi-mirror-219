""" shil.models.base
"""

import pydantic


class BaseModel(pydantic.BaseModel):
    """ """

    def update(self, **kwargs):
        return self.__dict__.update(**kwargs)

    class Config:
        arbitrary_types_allowed = True
        # frozen = True
