#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import (Column, String)
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if os.environ["HBNB_TYPE_STORAGE"] == "db":
        cities = relationship(
                "City", backref="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """Return list of cities related to the current State"""
            from models import storage
            cities = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities.append(city)
            return cities
