from fastapi import FastAPI
from app.routes import airport_routes

app = FastAPI()

app.include_router(airport_routes.router)

@app.on_event("startup")
async def startup_event():
    from app.utils.load_data import initialize_data
    await initialize_data()
