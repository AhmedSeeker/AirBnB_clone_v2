#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import (Table, Column, String, ForeignKey, Integer, Float)
from sqlalchemy.orm import relationship
import os
place_amenity = Table(
        "place_amenity", Base.metadata,
        Column("place_id", String(60),
               ForeignKey('places.id'), primary_key=True),
        Column("amenity_id", String(60),
               ForeignKey('amenities.id'), primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if os.environ['HBNB_TYPE_STORAGE'] == "db":
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        from models import storage

        @property
        def reviews(self):
            """Return all reviews related to the current place"""
            reviews = []
            for review in storage.all(Review):
                if review.place_id == self.id:
                    reviews.append(review)
            return reviews

        @amenities.setter
        def amenities(self, amenity):
            """Add an amenity to the current place"""
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)
