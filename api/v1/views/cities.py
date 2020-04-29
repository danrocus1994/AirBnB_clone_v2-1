#!/usr/bin/python3
"""
Index route for AirBnB clone v3 API v1
"""


from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities(state_id):
    """
    This route return a list of cities given by the status id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City)
    cities_list = []
    for key, city in cities.items():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    response = make_response(json.dumps(cities_list,
                                        indent=2,
                                        sort_keys=True), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def remove_city(city_id):
    """
    Handles the State removtion route,
    takes and id and uses storage to remove it
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    resp = make_response(json.dumps({}, indent=2, sort_keys=True),
                         200,
                         headers={"Content-Type": "application/json"})
    resp.headers['Content-Type'] = 'application/json'
    return resp
