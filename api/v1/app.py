#!/usr/bin/python3
"""
Flask Application server with view Blueprint
"""


from models import storage
from api.v1.views import app_views
from flask import Flask
import os


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.register_blueprint(app_views)
    host = os.getenv("HBNB_API_HOST")
    print(type(host), host)
    port = os.getenv("HBNB_API_PORT")
    app.run(host=host if host is not None else '0.0.0.0',
            port=port if port is not None else '5000',
            threaded=True)
