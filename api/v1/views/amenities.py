#!/usr/bin/python3
""" index file for flask """
from os import abort
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, request, abort
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_get():
    """Retrieves the list of all City objects"""
    amenities = storage.all('Amenity')
    list = []
    for amenity in amenities.values():
        list.append(amenity.to_dict())
    return jsonify(list), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_get(amenity_id=None):
    """Status json"""
    amenities = storage.all("Amenities")
    amenity = amenities.get('Amenity', + '.' + amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_amenity_by_id(amenity_id=None):
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_post():
    """Status delete"""
    result = request.get_json()
    if result is None:
        abort(400, {"Not a JSON"})
    if 'name' not in result:
        abort(400, {"Missing name"})
    obj_amenity = Amenity(name=result['name'])
    storage.new(obj_amenity)
    storage.save()
    return jsonify(obj_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id=None):
    result = request.get_json()
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, {"Not a JSON"})
    for key, value in result.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
