from flask import Flask
from app.routes.airports import airports_bp
from app.utils.load_data import initialize_data

def create_app():
    app = Flask(__name__)
    app.register_blueprint(airports_bp)

    with app.app_context():
        initialize_data()

    return app
