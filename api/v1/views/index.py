#!/usr/bin/python3
"""index views module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status', methods=['GET'])
def get_status():
    """return status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats_count():
    """return number of each object"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    counts = {}
    for key, obj in classes.items():
        counts[key] = storage.count(obj)
    return jsonify(counts)
