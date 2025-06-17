from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["airport_db"]  # nombre correcto de la base
collection = db["airports"]

def list_all_airports():
    return list(collection.find({}, {'_id': 0}))

def get_airport_by_iata(code):
    print(f"Buscando aeropuerto con código: {code}")
    doc = collection.find_one({"iata_faa": code}, {'_id': 0})
    if not doc:
        print(f"No encontrado por IATA, intentando por ICAO...")
        doc = collection.find_one({"icao": code}, {'_id': 0})
    return doc

def save_airport(data):
    # Asegurar que el documento tenga los campos iata_faa e icao
    if 'iata_faa' not in data or 'icao' not in data:
        raise ValueError("Faltan campos clave: 'iata_faa' o 'icao'")
    collection.insert_one(data)

def update_airport(code, data):
    # Intentar por iata_faa primero
    result = collection.update_one(
        {"iata_faa": code},
        {"$set": data}
    )
    if result.matched_count == 0:
        # Intentar por icao si no se encontró por iata_faa
        result = collection.update_one(
            {"icao": code},
            {"$set": data}
        )
    return result.modified_count

def delete_airport_by_iata(code):
    result = collection.delete_one({"iata_faa": code})
    if result.deleted_count == 0:
        result = collection.delete_one({"icao": code})
    return result.deleted_count
