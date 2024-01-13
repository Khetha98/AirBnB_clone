#!/usr/bin/python3
"""user module"""
from models.base_model import BaseModel


class User(BaseModel):
    """It creates the new user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
