#!/usr/bin/python3
"""It a state module

Has State() class that inherits from
BaseModel() class"""
from models.base_model import BaseModel

class State(BaseModel):
    """It a state of application

    Attributes:
        name
    """
    name = ""
