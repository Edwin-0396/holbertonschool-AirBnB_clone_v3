#!/usr/bin/python3
""" index file for flask """
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    """Status json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Stat"""
    count = 0
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    dict_count = {}
    for CLS in classes:
        count = models.storage.count(CLS)
        dict_count[CLS] = count
    return jsonify(dict_count)
