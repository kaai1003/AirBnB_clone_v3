#!/usr/bin/python3
"""Flask Web application Api module"""

from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask import Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': "Not found"}), 404


if __name__ == '__main__':
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_MYSQL_HOST')
    else:
        host = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = '5000'
    app.run(host, port, threaded=True)
