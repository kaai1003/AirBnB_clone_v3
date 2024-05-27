#!/usr/bin/python3
"""reviews views module"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
import models
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review

@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """retrieve all reviews"""
    for place in storage.all(City).values():
        if place.id == place_id:
            all_reviews = storage.all(Review)
            list_reviews = []
            for obj in all_reviews.values():
                if obj.place_id == place_id_id:
                    list_reviews.append(obj.to_dict())
            return jsonify(list_reviews)
        abort(404)