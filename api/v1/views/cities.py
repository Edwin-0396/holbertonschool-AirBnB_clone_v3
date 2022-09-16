#!/usr/bin/python3
"""cities.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """get information for all cities in states"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """get information for city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    city_new = request.get_json()
    if not city_new:
        abort(400, 'Not a JSON')
    if 'name' not in city_new:
        abort(400, 'Missing name')
    city = City(**city_new)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)





