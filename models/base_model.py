#!/usr/bin/python3

from datetime import datetime
import uuid
import models


class BaseModel:

    def __init__(self, *args, **kwargs):
        if kwargs:
            if '__class__' in kwargs:
                class_name = kwargs.pop('__class__')
                current_cls = BaseModel  # Default to BaseModel if the class is not found
                try:
                    current_cls = eval(class_name)
                except NameError:
                    pass

                for key, value in kwargs.items():
                    if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, key, value)
                self.id = kwargs.get('id', str(uuid.uuid4()))
                self.created_at = kwargs.get('created_at', datetime.now())
                self.updated_at = kwargs.get('updated_at', datetime.now())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        instance_dictionay = self.__dict__.copy()
        instance_dictionay['created_at'] = self.created_at.isoformat()
        instance_dictionay['updated_at'] = self.updated_at.isoformat()
        instance_dictionay['__class__'] = self.__class__.__name__
        return instance_dictionay
