#!/usr/bin/python3
"""
Place route for AirBnB clone v3 API v1
"""

from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
import json


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """
    This route retrieves the list of all place objects of a city
    """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify(error="Not found"), 404
    print(city.places)
    places = city.places
    places_list = []
    if places is not None:
        for place in places:
            places_list.append(place.to_dict())
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET'])
def place_by_id(place_id):
    """
    This route retrieves a place object
    @place_id: id of place
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify(error="Not found"), 404
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    """
    This route delete a place
    @place_id: id of place that will be deleted
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify(error="Not found"), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """
    This route create a new place
    @city_id: id of city to linked the place
    Require at least name and user_id
    Return the new Place object
    """
    storage_t = type(storage).__name__
    req = request.get_json()
    if req:
        city = storage.get(City, city_id)
        if city is None:
            return jsonify(error="Not found"), 404
        if 'user_id' in req:
            user = storage.get(User, req['user_id'])
            if user is None:
                return jsonify(error="Not found"), 404
        else:
            return jsonify(error="Missing user_id"), 400
        if 'name' in req:
            new_place = Place(**req)
            new_place.city_id = city_id
            if storage_t != "DBStorage":
                city.places_ids.append(new_place.id)
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    return jsonify(error="Not a JSON"), 400


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """
    This route update a place
    @place_id: id of place that will be updated
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify(error="Not found"), 404
    req = request.get_json()
    if req is None:
        return jsonify(error="Not a JSON"), 400
    for key, value in req.items():
        setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
