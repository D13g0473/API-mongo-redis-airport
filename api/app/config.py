import os

MONGO_DB = "airport_db"
MONGO_COLLECTION = "airports"

# Redis GEO y POP usando variables de entorno correctas
REDIS_GEO_HOST = os.getenv("REDIS_GEO_HOST", "localhost")
REDIS_GEO_PORT = int(os.getenv("REDIS_GEO_PORT", 6381))

REDIS_POP_HOST = os.getenv("REDIS_POP_HOST", "localhost")
REDIS_POP_PORT = int(os.getenv("REDIS_POP_PORT", 6380))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

POPULARITY_KEY = "airport_popularity"
