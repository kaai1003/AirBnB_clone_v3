#!/usr/bin/python3
"""state views module"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def all_states():
    """retrieve all states"""
    all_states = storage.all(State)
    list_states = []
    for obj in all_states.values():
        list_states.append(obj.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """retrive state based on id"""
    all_states = storage.all(State)
    for obj in all_states.values():
        if obj.id == state_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete state"""
    all_states = storage.all(State)
    for obj in all_states.values():
        if obj.id == state_id:
            storage.delete(obj)
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """create new state"""
    if request.is_json:
        dict = request.get_json()
        if "name" in dict.keys():
            new_state = State(**dict)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """update state"""
    state = storage.get(State, state_id)
    if state is not None:
        if request.is_json:
            inputs = request.get_json()
            for key, value in inputs.items():
                ignore = ['id', 'created_at', 'updated_at']
                if key not in ignore:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
        abort(400, "Not a JSON")
    abort(404)
