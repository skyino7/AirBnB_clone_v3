#!/usr/bin/python3
"""Places objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Return all places"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Return a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return "Not a JSON", 400
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if "name" not in data:
        abort(400, description="Missing name")
    new_place = Place(**data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return "Not a JSON", 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
