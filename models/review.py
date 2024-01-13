#!/usr/bin/python3
"""
Review module that.

Has Review class that inherits from BaseModel()
class
"""
from models.base_model import BaseModel

class Review(BaseModel):
    """ It a review of the place

    Attributes:
        text
        user_id
        place_id
    """

    text = ""
    user_id = ""
    place_id = ""
