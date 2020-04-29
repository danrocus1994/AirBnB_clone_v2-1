#!/usr/bin/python3
"""
Amenities route for AirBnB clone v3 API v1
"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
import json


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """
    This route retrieves the list of all amenity objects
    """
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_by_id(amenity_id):
    """
    This route retrieves a amenity object
    @amenity_id: id of amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify(error="Not found"), 404
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """
    This route delete a amenity
    @amenity_id: id of amenity that will be deleted
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify(error="Not found"), 404
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
    This route create a new amenity
    Require at least name
    """
    if request.is_json:
        req = request.get_json()
        if req['name']:
            new_amenity = Amenity(**req)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    return jsonify(error="Not a JSON"), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    This route update a amenity
    @amenity_id: id of Amenity that will be updated
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify(error="Not found"), 404
    if request.is_json is None:
        return jsonify(error="Not a JSON"), 400
    req = request.get_json()
    for key, value in req.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
