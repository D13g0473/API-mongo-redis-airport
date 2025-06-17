from app import create_app
from flask_cors import CORS
app = create_app()
CORS(app, origins=["http://localhost:*"], allow_headers=["Content-Type","Access-Control-Allow-Origin"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
