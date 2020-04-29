#!/usr/bin/python3
"""
Init for views API Blueprint
"""


from api.v1.views.index import *
from api.v1.views.cities import *
from api.v1.views.states import *
from flask import Blueprint

app_views = Blueprint('api_v1', __name__, url_prefix='/api/v1')
