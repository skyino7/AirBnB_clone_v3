#!/usr/bin/python3
"""Views for the cities"""
from api.v1.views import app_views
from models import storage
from models.city import City
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
        return "Not a JSON", 400
    if "name" not in data:
        abort(400, description="Missing name")
    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    city = City.query.get(city_id)
    if not city:
        return jsonify({'error': 'Not found'}), 404

    for key, value in data.items():
        if key not in ['city_id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict())
