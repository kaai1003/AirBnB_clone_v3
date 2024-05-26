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
        if obj.id == city_id_id:
            storage.delete(obj)
            return jsonify({}), 200
    abort(404)
