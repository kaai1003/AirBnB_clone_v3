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
                if obj.place_id == place_id:
                    list_reviews.append(obj.to_dict())
            return jsonify(list_reviews)
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """retrive review based on id"""
    all_reviews = storage.all(Review)
    for obj in all_reviews.values():
        if obj.id == review_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete review"""
    all_reviews = storage.all(Review)
    for obj in all_reviews.values():
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """create new review"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            if request.is_json:
                dict = request.get_json()
                if 'user_id' not in dict.keys():
                    abort(400, "Missing user_id")
                if 'text' not in dict.keys():
                    abort(400, "Missing text")
                for user in storage.all(User).values():
                    if user.id == dict['user_id']:
                        new_review = Review(**dict)
                        new_review.place_id = place_id
                        new_review.save()
                        return jsonify(new_review.to_dict()), 201
                abort(404)
            abort(400, "Not a JSON")
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """update review"""
    review = storage.get(Review, review_id)
    if review is not None:
        if request.is_json:
            inputs = request.get_json()
            for key, value in inputs.items():
                ignore = ['id', 'user_id', 'place_id',
                          'created_at', 'updated_at']
                if key not in ignore:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
        abort(400, "Not a JSON")
    abort(404)
