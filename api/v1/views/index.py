#!/usr/bin/python3
"""index views module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def get_status():
    """return status ok"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats_count():
    """return number of each object"""
    return storage.count()