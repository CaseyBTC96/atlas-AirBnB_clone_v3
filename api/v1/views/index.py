#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon March 18 18:09:23 2024
@authors: Casey Paul
          Crystal
"""
from flask import jsonify, Blueprint
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ check the status of route """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """retrieves the number of each objects by type
    """
    objects = {"amenities": 'Amenity',
            "cities": 'City',
            "places": 'Place',
            "reviews": 'Review',
            "states": 'State',
            "users": 'User'
    }
    stats = {}
    for key, value in objects.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
