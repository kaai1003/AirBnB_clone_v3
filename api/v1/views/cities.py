#!/usr/bin/python3
"""state views module"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
import models
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def state_cities(state_id):
    """retrieve all cities of state"""
    all_states = storage.all(State)
    list_cities = []
    for obj in all_states.values():
        if obj.id == state_id:
            if models.storage_t != 'db':
                for city in obj.cities:
                    list_cities.append(city.to_dict())
                return jsonify(list_cities)
            for city in storage.all(City).values():
                if city.state_id == obj.id:
                    list_cities.append(city.to_dict())
            return jsonify(list_cities)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """retrive city based on id"""
    all_cities = storage.all(City)
    for obj in all_cities.values():
        if obj.id == city_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete city"""
    all_cities = storage.all(City)
    for obj in all_cities.values():
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create new city"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            if request.is_json:
                dict = request.get_json()
                if "name" in dict.keys():
                    new_city = City(**dict)
                    new_city.save()
                    return jsonify(new_city.to_dict()), 201
                abort(400, "Missing name")
            abort(400, "Not a JSON")
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """update city"""
    cities = storage.all(City)
    for city in cities.value():
        if city.id == city_id:
            if request.is_json:
                inputs = request.get_json()
                for key, value in inputs.items():
                    ignore = ['id', 'state_id', 'created_at', 'updated_at']
                    if key not in ignore:
                        setattr(city, key, value)
                    city.save()
                    return jsonify(city.to_dict()), 200
            abort(400, "Not a JSON")
    abort(404)
