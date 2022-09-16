#!/usr/bin/python3
""" index file for flask """
from crypt import methods
from os import abort
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_get(state_id=None):
    """Retrieves the list of all City objects"""
    states = storage.all("State")
    state = states.get('State' + '.' + state_id)
    if state in None:
        abort(404)
    list = []
    cities = storage.all('City')
    for city in cities.values():
        if city.state_id == state_id:
            list.append(city.to_dict())
    return jsonify(list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_get(state_id=None):
    """Status json"""
    dict_all = storage.all("State")
    list = []
    if state_id is not None:
        for states_values in dict_all.values():
            if states_values.id == state_id:
                return jsonify(states_values.to_dict())
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deletes_cities_by_id(city_id):
    city_obj = storage.get('City', city_id)
    if not city_obj:
        abort(404)
    city_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/<state_id>/cities', methods=['POST'], strict_slashes=False)
def cities_post(state_id=None):
    """Status delete"""
    dic_state = storage.all(State)
    state = dic_state.get('State' + '.' + state_id)
    if state is None:
        abort(400)
    result = request.get_json()
    if result is None:
        abort(400, {"Not a JSON"})
    if 'name' not in result:
        abort(400, {"Missing name"})
    city_ins = State(name=result['name'])
    storage.new(city_ins)
    storage.save()
    return jsonify(city_ins.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id=None):
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    if not request.get_json():
        abort(400, {"Not a JSON"})
    result = request.get_json()
    for key, value in result.items():
        if key in ['id', 'state_id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(city_obj, key, value)
    storage.save()
    return jsonify(city_obj.to_dict()), 200
