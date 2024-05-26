#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


classes = {"amenities": Amenity, "cities": City,"places": Place,
           "reviews": Review, "states": State, "users": User}
counts ={}
for key, obj in classes.items():
    counts[key] = storage.count(obj)
print(counts)
