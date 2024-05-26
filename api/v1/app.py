#!/usr/bin/python3
"""Flask Web application Api module"""

from flask import Flask
from flask import Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


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
