#!/usr/bin/python3
"""Amenity views module"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """retrieve all amenities"""
    all_amenities = storage.all(Amenity)
    list_amenities = []
    for obj in all_amenities.values():
        list_amenities.append(obj.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """retrive amenity based on id"""
    all_amenities = storage.all(Amenity)
    for obj in all_amenities.values():
        if obj.id == amenity_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity"""
    all_amenities = storage.all(Amenity)
    for obj in all_amenities.values():
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """create new amenity"""
    if request.is_json:
        dict = request.get_json()
        if "name" in dict.keys():
            new_amenity = Amenity(**dict)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        if request.is_json:
            inputs = request.get_json()
            for key, value in inputs.items():
                ignore = ['id', 'created_at', 'updated_at']
                if key not in ignore:
                    setattr(amenity, key, value)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
        abort(400, "Not a JSON")
    abort(404)
