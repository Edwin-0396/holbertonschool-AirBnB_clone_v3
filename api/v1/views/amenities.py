#!/usr/bin/python3
"""cities.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from holbertonschool-AirBnB_clone_v3.models import amenity
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieve_amenities(amenities):
    """Retrieves the list of all Amenity objects"""
    all_amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenity_obj(amenity_id):
    """Retrieve an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """Method to delete an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    amenity.save()
    return (jsonify({})), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity(amenities):
    """Transform the HTTP request to a dictionary"""
    ameni = request.get_json()
    if ameni is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = amenities.Amenity(**ameni)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    amenity.save()
    return jsonify(amenity.to_dict())
