#!/usr/bin/python3
""" index file for flask """
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
import os
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


app = Flask(__name__)

@app_views.route('/status')
def status():
    """Status json"""
    return jsonify({"status":"OK"})

@app_views.route('/stats')
def stats():
    """Stat"""
    count = 0
    classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}
    dict_count = {}
    for CLS in classes:
        count = models.storage.count(CLS)
        dict_count[CLS] = count
    return jsonify(dict_count)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='5000')