from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from os import getenv

time_fmt = "%Y-%m-%dT%H:%M:%S.%f"

if getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializes the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                setattr(self, key, value)
            try:
                if 'created_at' in kwargs:
                    self.created_at = datetime.strptime(kwargs['created_at'], time_fmt)
                if 'updated_at' in kwargs:
                    self.updated_at = datetime.strptime(kwargs['updated_at'], time_fmt)
            except ValueError:
                self.created_at = datetime.utcnow()
                self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{:s}] ({:s}) {}'.format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """Convert instance into dict format and returns it with all values"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        if '_password' in new_dict:
            new_dict['password'] = new_dict['_password']
            new_dict.pop('_password', None)
        if 'amenities' in new_dict:
            new_dict.pop('amenities', None)
        if 'reviews' in new_dict:
            new_dict.pop('reviews', None)
        new_dict["__class__"] = self.__class__.__name__
        new_dict.pop('_sa_instance_state', None)
        if not save_to_disk:
            new_dict.pop('password', None)
        return new_dict

    def delete(self):
        """Delete current instance from storage by calling this method"""
        models.storage.delete(self)
