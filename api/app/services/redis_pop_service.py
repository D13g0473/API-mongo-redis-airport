import redis
from app.config import *
from app.services.mongo_service import collection
from app.config import REDIS_POP_HOST, REDIS_POP_PORT, POPULARITY_KEY

r = redis.Redis(host=REDIS_POP_HOST, port=REDIS_POP_PORT)

def increment_popularity(iata):
    r.zincrby(POPULARITY_KEY, 1, iata)

def remove_from_popularity(iata):
    r.zrem(POPULARITY_KEY, iata)

def get_top_popular():
    raw = r.zrevrange(POPULARITY_KEY, 0, 10, withscores=True)
    result = []

    for member, score in raw:
        code = member.decode("utf-8")
        airport = collection.find_one(
            {"$or": [{"iata_faa": code}, {"icao": code}]},
            {"_id": 0}
        )

        if airport:
            airport["popularity"] = score
            result.append(airport)
        else:
            # si no hay coincidencia, devolvemos solo el código y el score
            result.append({"code": code, "popularity": score})

    return result
