#!/usr/bin/python3
"""
Index route for AirBnB clone v3 API v1
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """
    This route return a success status in JSON format
    """
    return jsonify(status="OK"), 200
