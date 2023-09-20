#!/usr/bin/python3
"""Module for objects storage in a database"""
from sqlalchemy import create_engine
from models.base_model import Base
import os


class DBStorage:
    """Define DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            os.environ["HBNB_MYSQL_USER"],
            os.environ["HBNB_MYSQL_PWD"],
            os.environ["HBNB_MYSQL_HOST"],
            os.environ["HBNB_MYSQL_DB"]),
            pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects depending
        or not of the class name"""
        dictionary = {}
        objects = []
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = self.__session.query(
                    User, State, City, Amenity, Place, Review).all()
        for obj in objects:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            dictionary[key] = obj
        return dictionary

    def new(self, obj):
        """Add the object to the current database"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Ccommit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the current database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and a session for it"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from sqlalchemy.orm import sessionmaker, scoped_session
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Session)
        self.__session = Session()
