#!/usr/bin/python3
"""Views for the cities"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Return all cities"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Return a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"Not a JSON"}), 400
    if "name" not in data:
        abort(400, description="Missing name")
    state = State.query.get(state_id)
    new_city = City(name=data["name"], state_id=state_id)
    for key, value in data.items():
        if key != 'name':
            setattr(new_city, key, value)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            settattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

