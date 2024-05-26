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
all_states = storage.all(State)
list_states = []
for obj in all_states.values():
    list_states.append(obj.to_dict())
print(list_states)