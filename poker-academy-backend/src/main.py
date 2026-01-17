# src/main.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime
from urllib.parse import quote_plus

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_folder, ".env"))

from src.routes.user_routes import user_bp
from src.routes.auth_routes import auth_bp
from src.routes.favorites_routes import favorites_bp
from src.routes.playlist_routes import playlist_bp
from src.routes.particao_routes import particao_bp
from src.routes.password_reset_routes import password_reset_bp
from src.routes.graphs_routes import graphs_bp
from src.routes.admin_graphs_routes import admin_graphs_bp
from src.routes.upload_routes import upload_bp
from src.routes.database_routes import database_bp
from src.models import db, Classes
from src.password_reset_model import PasswordResetToken  # Importar para criar tabela
from src.routes.class_routes import class_bp

app = Flask(__name__)
CORS(app,
     origins=["http://localhost:3000", "http://localhost:3001"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Usar DATABASE_URL se disponível (Supabase/Produção)
    print(f"[DB] Usando DATABASE_URL (PostgreSQL): {DATABASE_URL[:50]}...")
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    # PostgreSQL local para desenvolvimento (ou SQLite como fallback)
    DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "poker_academy")
    connection_string = f"postgresql://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"[DB] Usando PostgreSQL local: {connection_string}")
    app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB max file size

# Configurar pasta de uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'videos'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'graphs'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'leaks'), exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

app.register_blueprint(class_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(favorites_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(particao_bp)
app.register_blueprint(password_reset_bp)
app.register_blueprint(graphs_bp)
app.register_blueprint(admin_graphs_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(database_bp)

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

