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
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """It updates public instance attributes"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Gives a dictionary derived from __dict__"""
        instance_dictionay = self.__dict__.copy()
        instance_dictionay['created_at'] = self.created_at.isoformat()
        instance_dictionay['updated_at'] = self.updated_at.isoformat()
        instance_dictionay['__class__'] = self.__class__.__name__
        return instance_dictionay
