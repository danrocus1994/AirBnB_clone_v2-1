#!/usr/bin/python3
"""
Index route for AirBnB clone v3 API v1
"""


from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, Response, abort, request
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities(state_id):
    """
    This route return a list of cities given by the status id
    """
    cities = storage.all(City)
    cities_list = []
    for key, city in cities.items():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    if len(cities_list) == 0:
        abort(404)
    return Response(json.dumps(cities_list, indent=2, sort_keys=True), 200
                    mimetype='application/json')


@app_views.route('/cities/<city_id>', methods=['GET'])
def single_city(city_id):
    """
    Return the Json of a City by its id
    """
    print(city_id)
    city = storage.get(City, city_id)
    print(city)
    if city is None:
        print("City is None")
        abort(404)
    city = city.to_dict()
    return Response(json.dumps(city, indent=2, sort_keys=True), 200,
                    mimetype='application/json')


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def remove_city(city_id):
    """
    Handles the State removtion route,
    takes and id and uses storage to remove it
    """
    print("Delete ", city_id)
    city = storage.get(City, city_id)
    print(city)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return Response(json.dumps({}, indent=2, sort_keys=True), 200,
                    mimetype='application/json')


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
    Creates a new city in the State
    given by state_id
    """
    req = request.get_json()
    if req is None:
        return jsonify(error="Not a JSON"), 400
    if not "name" in req:
        return jsonify(error="Missing name"), 404
    req["state_id"] = state_id
    print(req)
    city = City(**req)
    print(city, type(city))
    storage.new(city)
    storage.save()
    return Response(json.dumps(city.to_dict(), indent=2, sort_keys=True), 201,
                    mimetype='application/json')


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Update the city given by city_id
    returns error if there is no name or if request is not a proper dict
    """
    req = request.get_json()
    if req is None:
        return jsonify(error="Not a JSON"), 400
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        for key in req.keys():
            avoid = [key != "id",
                     key != "state_id",
                     key != "updated_at",
                     key in city.to_dict()
                     ]
            if all(avoid):
                setattr(city, key, req[key])
    except Exception as e:
        abort(404)
    storage.save()
    return Response(json.dumps(city.to_dict(), indent=2, sort_keys=True), 200,
                    mimetype='application/json')


@app_views.route('/states/<state_id>', methods=['DELETE'])
def remove_state(state_id):
    """
    Handles the State remotion route,
    takes and id and uses storage to remove it
    """
    print("Delete ", state_id)
    storage.delete(storage.get(state_id))
    return Response(json.dumps({}, indent=2, sort_keys=True), 200,
                    mimetype='application/json')
