#!/usr/bin/python3
"""
Index route for AirBnB clone v3 API v1
"""


from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, make_response, request
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities(state_id):
    """
    This route return a list of cities given by the status id
    """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify(error="Not found"), 404
    cities = storage.all(City)
    cities_list = []
    for key, city in cities.items():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    resp = make_response(json.dumps(cities_list, sort_keys=True), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp
