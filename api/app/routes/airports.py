from flask import Blueprint, request, jsonify
from app.services.mongo_service import *
from app.services.redis_geo_service import *
from app.services.redis_pop_service import *

airports_bp = Blueprint('airports', __name__)

@airports_bp.route("/airports", methods=["GET"])
def get_airports():
    return jsonify(list_all_airports())

@airports_bp.route("/airports/<iata>", methods=["GET"])
def get_airport(iata):
    increment_popularity(iata)
    return jsonify(get_airport_by_iata(iata))

@airports_bp.route("/airports", methods=["POST"])
def create_airport():
    data = request.json
    save_airport(data)
    add_to_geo(data)
    return jsonify({"message": "Airport created"}), 201

@airports_bp.route("/airports/<iata>", methods=["PUT"])
def update_airport_route(iata):
    data = request.json
    update_airport(iata, data)
    return jsonify({"message": "Airport updated"})

@airports_bp.route("/airports/<iata>", methods=["DELETE"])
def delete_airport(iata):
    delete_airport_by_iata(iata)
    remove_from_geo(iata)
    remove_from_popularity(iata)
    return jsonify({"message": "Airport deleted"})

@airports_bp.route("/airports/nearby", methods=["GET"])
def get_nearby():
    lat = float(request.args.get("lat"))
    lng = float(request.args.get("lng"))
    radius = float(request.args.get("radius", 2000))
    data = get_nearby_airports(lat, lng, radius)
    return jsonify(data)

@airports_bp.route("/airports/popular", methods=["GET"])
def get_popular():
    return jsonify(get_top_popular())
