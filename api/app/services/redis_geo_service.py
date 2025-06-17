import redis
from app.services.mongo_service import collection
from app.config import REDIS_GEO_HOST, REDIS_GEO_PORT

r = redis.Redis(host=REDIS_GEO_HOST, port=REDIS_GEO_PORT)

def add_to_geo(airport):
    r.geoadd("airports-geo", (airport["lng"], airport["lat"], airport["iata_faa"]))

def remove_from_geo(iata):
    r.zrem("airports-geo", iata)

def get_nearby_airports(lat, lng, radius):
    raw = r.georadius("airports-geo", lng, lat, radius, unit="km", withdist=True)
    result = []
    for item in raw:
        if isinstance(item, tuple):
            raw_code = item[0]
            distance = float(item[1])
        else:
            raw_code = item
            distance = None

        # Decodifica si es bytes
        code = raw_code[0].decode("utf-8") if isinstance(raw_code[0], bytes) else raw_code[0]
        distance = raw_code[1]
        airport = collection.find_one(
            {"$or": [{"iata_faa": code}, {"icao": code}]},
            {"_id": 0}
        )

        if airport:
            # Limpia cualquier valor bytes dentro del documento
            airport_clean = {
                k: (v.decode("utf-8") if isinstance(v, bytes) else v)
                for k, v in airport.items()
            }
            airport_clean["distance_km"] = distance
            result.append(airport_clean)
        else:
            result.append({
                "code": code,
                "distance_km": distance
            })
    return result


def json_safe(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="ignore")
    elif isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [json_safe(item) for item in obj]
    else:
        return obj
