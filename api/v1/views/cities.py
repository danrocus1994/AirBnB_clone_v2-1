#!/usr/bin/python3
"""
Index route for AirBnB clone v3 API v1
"""


from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
import json


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET'])
def cities(state_id):
    """
    This route return a list of cities given by the status id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([cit.to_dict() for cit in state.cities])


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def single_city(city_id):
    """
    Return the Json of a City by its id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def remove_city(city_id):
    """
    Handles the State removtion route,
    takes and id and uses storage to remove it
    """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify(error="Not found"), 404
    resp = make_response(json.dumps({}), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """
    Creates a new city in the State
    given by state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if req is None or type(req) != dict:
        return jsonify(error="Not a JSON"), 400
    if "name" not in req:
        return jsonify(error="Missing name"), 400
    req["state_id"] = state_id
    city = City(**req)
    storage.new(city)
    storage.save()
    resp = make_response(city.to_dict(), 201)
    resp.headers['Content-Type'] = 'application/json'
    return resp
