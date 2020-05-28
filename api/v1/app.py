#!/usr/bin/python3
"""
Flask Application server with view Blueprint
"""


from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, request
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """
    Defines not found json response
    """
    print("Handling Error")
    print(request)
    print(dir(resquest))
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST")
    print(type(host), host)
    port = os.getenv("HBNB_API_PORT")
    app.run(host=host if host is not None else '0.0.0.0',
            port=port if port is not None else '5000',
            threaded=True)
