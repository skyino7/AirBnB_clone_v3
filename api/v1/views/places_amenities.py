#!/usr/bin/python3
"""Places amenities objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, request, abort


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """Return all amenities"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Delete a amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if storage.__class__.__name__ == "DBStorage":
        place.amenities.remove(amenity)
        storage.save()
    else:
        place.amenity_ids.remove(amenity_id)
        storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity(place_id, amenity_id):
    """Create a amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if storage.__class__.__name__ == "DBStorage":
        place.amenities.append(amenity)
        storage.save()
    else:
        place.amenity_ids.append(amenity_id)
        storage.save()

    return jsonify(amenity.to_dict()), 201
