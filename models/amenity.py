#!/usr/bin/python3
"""It the amenity module
It plays a role of defining Amenity()
which inherits from the BaseModel() class
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """It an amenity given by a place
    
    Attributes:
    name
    """

    name = ""
