#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from os import getenv
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    '''
        Base class for other classes to be used for the duration.
    '''
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        '''
            Initialize public instance attributes.
        '''
        if (len(kwargs) == 0):
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get("created_at"):
                kwargs["created_at"] = datetime.strptime(
                    kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.now()
            if kwargs.get("created_at"):
                kwargs["updated_at"] = datetime.strptime(
                    kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.now()
            for key, val in kwargs.items():
                if "__class__" not in key:
                    setattr(self, key, val)
            if not self.id:
                self.id = str(uuid.uuid4())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """delete obj"""
        models.storage.delete(self)
