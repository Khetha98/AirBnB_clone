#!/usr/bin/python3
"""This a module  base.py"""
from datetime import datetime
import uuid
import models


class BaseModel:
    """
    It defines attributes or methods that are common
    to other classes
    """

    def __init__(self, *args, **kwargs):
        """Instantiates an object with its attributes."""
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
            return


        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        models.storage.new(self)

    def __str__(self):
        """
        Gives out a string representation
        of the instance
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def save(self):
        """It updates public instance attributes"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Gives a dictionary derived from __dict__"""
        dict = {**self.__dict__}
        dict['__class__'] = type(self).__name__
        dict['created_at'] = dict['created_at'].isoformat()
        dict['updated_at'] = dict['updated_at'].isoformat()

        return dict
