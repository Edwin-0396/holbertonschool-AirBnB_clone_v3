#!/usr/bin/python3
""" index file for flask """
from crypt import methods
from os import abort
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, request
from models import storage
from models.state import State

@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def states_get(state_id=None):
	"""Status json"""
	dict_all = storage.all("State")
	list = []
	for states_values in dict_all.values():
		list.append(states_values.to_dict())
	return jsonify(list)

@app_views.route('/states/<state_id>', methods = ['GET'], strict_slashes = False)
def states_get_id(state_id=None):
	"""Status json"""
	dict_all = storage.all("State")
	list = []
	if state_id is not None:
		for states_values in dict_all.values():
			if states_values.id == state_id:
				return jsonify(states_values.to_dict())
		abort(404)

@app_views.route('/states/<state_id>', methods = ['DELETE'], strict_slashes = False)
def status_delete(state_id=None):
	"""Status delete"""
	state_obj = storage.get(State, state_id)
	if state_id == None:
		abort(404)
	state_obj.delete()
	storage.save()
	return ({}),200

@app_views.route('/states', methods = ['POST'], strict_slashes = False)
def states_post(state_id=None):
	"""Status delete"""
	result = request.get_json()
	if result is None:
		abort(404, {"Not a JSON"})
	if 'name' not in result:
		abort(404, {"Missing name" })
	state_ins = State(name=result['name'])
	storage.new(state_ins)
	storage.save()
	return jsonify(state_ins.to_dict()), 201