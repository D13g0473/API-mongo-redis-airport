import json
import os
from pymongo import MongoClient
import redis
from app.config import *

def initialize_data():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    # Cargar datos desde Mongo (ya deberían estar insertados previamente)
    data = list(collection.find({}, {'_id': 0}))
    if not data:
        # Si Mongo está vacío, intentamos cargar desde el archivo JSON
        print("⚠️ Mongo no tiene datos. Cargando desde airports.json...")
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'airports.json'))

        with open(json_path) as f:
            data = json.load(f)
            if not data:
                print("❌ No se pudieron cargar datos desde airports.json.")
                return
            collection.insert_many(data)
        print(f"✅ Insertados {len(data)} documentos en Mongo.")

    # Cargar datos geoespaciales en Redis Geo
    r = redis.Redis(host=REDIS_GEO_HOST, port=REDIS_GEO_PORT)
    count = 0
    for airport in data:
        ident = airport.get("iata_faa") or airport.get("icao")
        if not ident:
            print(f"⚠️ Aeropuerto sin código identificador: {airport.get('name')} - {airport.get('city')}")
            continue

        lat = airport.get("lat")
        lng = airport.get("lng")

        if not is_valid_coords(lat, lng):
            print(f"❌ Coordenadas inválidas para {ident}: lat={lat}, lng={lng}")
            continue

        try:
            r.geoadd("airports-geo", (lng, lat, ident))
            count += 1
        except Exception as e:
            print(f"❌ Error al agregar {ident} a Redis GEO: {e}")

    print(f"✅ Cargados {count} aeropuertos en Redis GEO.")

    # Inicializar clave de popularidad en Redis
    r_pop = redis.Redis(host=REDIS_POP_HOST, port=REDIS_POP_PORT)
    r_pop.expire(POPULARITY_KEY, 86400)
    print("✅ Popularidad inicializada en Redis POP.")

def is_valid_coords(lat, lng):
    return (
        isinstance(lat, (int, float)) and isinstance(lng, (int, float)) and
        -85.05112878 <= lat <= 85.05112878 and
        -180 <= lng <= 180
    )
