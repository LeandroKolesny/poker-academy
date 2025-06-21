# src/main.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_folder, ".env"))

from src.routes.user_routes import user_bp
from src.routes.auth_routes import auth_bp
from src.routes.favorites_routes import favorites_bp
from src.routes.playlist_routes import playlist_bp
from src.routes.particao_routes import particao_bp
from src.models import db, Classes
from src.routes.class_routes import class_bp

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001"], supports_credentials=True)

# Configuração do banco de dados MySQL
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "poker_academy")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

# Configuração do banco de dados MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB max file size

db.init_app(app)

app.register_blueprint(class_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(favorites_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(particao_bp)

@app.route("/")
def home():
    return jsonify(message="Bem-vindo à API da Poker Academy!")

@app.route("/api/health")
def health_check():
    """Endpoint para verificar se a aplicação está funcionando"""
    try:
        # Testar conexão com banco
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected',
            'message': 'API está funcionando!'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'disconnected',
            'error': str(e),
            'message': 'API com problemas!'
        }), 500



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

