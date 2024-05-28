#!/usr/bin/python3
"""places views module"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
import models
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def city_places(city_id):
    """retrieve all places of city"""
    for city in storage.all(City).values():
        if city.id == city_id:
            all_places = storage.all(Place)
            list_places = []
            for obj in all_places.values():
                if obj.city_id == city_id:
                    list_places.append(obj.to_dict())
            return jsonify(list_places)
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """retrive place based on id"""
    all_places = storage.all(Place)
    for obj in all_places.values():
        if obj.id == place_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete place"""
    all_places = storage.all(Place)
    for obj in all_places.values():
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create new place"""
    for city in storage.all(City).values():
        if city.id == city_id:
            if request.is_json:
                dict = request.get_json()
                if 'user_id' not in dict.keys():
                    abort(400, "Missing user_id")
                if 'name' not in dict.keys():
                    abort(400, "Missing name")
                for user in storage.all(User).values():
                    if user.id == dict['user_id']:
                        new_place = Place(**dict)
                        new_place.city_id = city_id
                        new_place.save()
                        return jsonify(new_place.to_dict()), 201
                abort(404)
            abort(400, "Not a JSON")
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is not None:
        if request.is_json:
            inputs = request.get_json()
            for key, value in inputs.items():
                ignore = ['id', 'user_id', 'city_id',
                          'created_at', 'updated_at']
                if key not in ignore:
                    setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict()), 200
        abort(400, "Not a JSON")
    abort(404)
