#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon March 18  18:20:21
@authors: Casey Paul
          Crystal
"""
from flask import Blueprint, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
                    
@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_by_state(state_id):
    """Create a new view for City objects that handles all default
    RestFul API actions.
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or not isinstance(post, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        new_city = City(**post_data)
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def city(city_id):
    """Retrieves a city object with a specific id"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
        
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        city = storage.get('City', city_id)
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or not isinstance(put, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
                storage.save()
        return jsonify(city.to_dict()), 200
