#!/usr/bin/python3
"""This a city module that defines a City()
class which inherits from the BaseModel() class"""

from models.base_model import BaseModel

class City(BaseModel):
    """
    It a city 
    Attributes:
        name
        state_id
    """
    name = ""
    state_id = ""
