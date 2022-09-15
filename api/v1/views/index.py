#!/usr/bin/python3
""" index file for flask """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=["GET"], strict_slashes=False)
def views_route():
    return jsonify({"status": "OK"})
