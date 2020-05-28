#!/usr/bin/python3
"""
Index route for AirBnB clone v3 API v1
"""


from api.v1.views import app_views
from models import storage
from models.user import User
from models.state import State
from flask import jsonify, request, abort, Response
import json


@app_views.route("/users", methods=['GET'])
def get_all_users():
    """
    Returns the JSON representation for each User
    """
    users = storage.all(User)
    # print(users)
    # return jsonify([us.to_dict() for key, us in users.items()])
    r = [us.to_dict() for key, us in users.items()]
    return Response(json.dumps(r), mimetype='application/json')

@app_views.route("/users/<user_id>", methods=['GET'])
def get_one_user(user_id):
    """
    Return one user by its id
    @user_id: the user id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_one_user(user_id):
    """
    Deletes one user by its id
    @user_id: the user id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users",
                 strict_slashes=False,
                 methods=['POST'])
def create_user():
    """
    Creates a new User
    """
    req = request.get_json()
    if not req:
        return jsonify(error="Not a JSON"), 400
    if "password" not in req:
        return jsonify(error="Missing password"), 400
    if "email" not in req:
        return jsonify(error="Missing email"), 400
    n_user = User(**req)
    storage.new(n_user)
    storage.save()
    return jsonify(n_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    """
    Update the user given by user_id
    returns error if there is no email or password,
    or if request is not a proper JSON
    """
    req = request.get_json()
    if not req or type(req) != dict:
        return jsonify(error="Not a JSON"), 400
    user = storage.get(User, user_id)
    if user is not None:
        for key in req.keys():
            setattr(user, key, req[key])
        storage.save()
        return jsonify(user.to_dict()), 200
    abort(404)
