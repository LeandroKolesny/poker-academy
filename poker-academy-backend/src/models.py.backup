# src/models.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAlchemyEnum
import enum
from datetime import datetime # Para default=datetime.utcnow ou similar se db.func.current_timestamp() não for o desejado

db = SQLAlchemy()

class UserType(enum.Enum):
    admin = "admin"
    student = "student"

class ClassCategory(enum.Enum):
    preflop = "preflop"
    postflop = "postflop"
    mental = "mental"
    icm = "icm"

class VideoType(enum.Enum):
    youtube = "youtube"  # Temporário para compatibilidade
    local = "local"

class MonthEnum(enum.Enum):
    jan = "jan"
    fev = "fev"
    mar = "mar"
    abr = "abr"
    mai = "mai"
    jun = "jun"
    jul = "jul"
    ago = "ago"
    set = "set"
    out = "out"
    nov = "nov"
    dez = "dez"

class Particoes(db.Model):
    __tablename__ = "particoes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text, nullable=True)
    ativa = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'ativa': self.ativa,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at and hasattr(self.updated_at, 'isoformat') else str(self.updated_at) if self.updated_at else None
        }

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False) # Nome real do usuário
    username = db.Column(db.String(100), nullable=False, unique=True) # Nome de usuário único
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False) # Senha hasheada
    type = db.Column(SQLAlchemyEnum(UserType), nullable=False, default=UserType.student) # Tipo de usuário
    particao_id = db.Column(db.Integer, db.ForeignKey('particoes.id'), nullable=False) # Chave estrangeira obrigatória
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Data de registro
    last_login = db.Column(db.DateTime, nullable=True)
    first_login = db.Column(db.Boolean, nullable=False, default=True) # True = precisa alterar senha no primeiro login

    # Relacionamento
    particao_obj = db.relationship('Particoes', backref='users')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'type': self.type.value if self.type else None,
            'particao_id': self.particao_id,
            'particao_nome': self.particao_obj.nome if self.particao_obj else None,
            'register_date': self.register_date.isoformat() if self.register_date and hasattr(self.register_date, 'isoformat') else str(self.register_date) if self.register_date else None,
            'last_login': self.last_login.isoformat() if self.last_login and hasattr(self.last_login, 'isoformat') else str(self.last_login) if self.last_login else None
            # Não inclua password_hash no to_dict por segurança
        }

class Classes(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False) # Mantido como Date
    category = db.Column(SQLAlchemyEnum(ClassCategory), nullable=True)  # Categoria agora é opcional
    video_type = db.Column(SQLAlchemyEnum(VideoType), nullable=False, default=VideoType.local)
    video_path = db.Column(db.String(255), nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=5)
    views = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Data de criação da aula

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "instructor": self.instructor,
            "date": self.date.isoformat() if self.date else None,
            "category": self.category.value if self.category else None,
            "video_type": self.video_type.value if self.video_type else None,
            "video_path": self.video_path,
            "priority": self.priority,
            "views": self.views,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class UserProgress(db.Model):
    __tablename__ = "user_progress"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id", ondelete="CASCADE"), primary_key=True)
    progress = db.Column(db.Integer, nullable=False, default=0)
    watched = db.Column(db.Boolean, nullable=False, default=False)
    last_watched = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    video_time = db.Column(db.Float, nullable=False, default=0.0)  # Tempo atual em segundos

class Favorites(db.Model):
    __tablename__ = "favorites"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id", ondelete="CASCADE"), primary_key=True)

class Playlists(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

class PlaylistClasses(db.Model):
    __tablename__ = "playlist_classes"
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id", ondelete="CASCADE"), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id", ondelete="CASCADE"), primary_key=True)

class ClassViews(db.Model):
    __tablename__ = "class_views"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    viewed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'class_id': self.class_id,
            'viewed_at': self.viewed_at.isoformat() if self.viewed_at else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }

class StudentGraphs(db.Model):
    __tablename__ = "student_graphs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    month = db.Column(SQLAlchemyEnum(MonthEnum), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relacionamentos removidos para evitar problemas na exclusão

    # Constraint única para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('student_id', 'month', 'year', name='unique_student_month_year'),)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else None,
            'month': self.month.value if self.month else None,
            'year': self.year,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class StudentLeaks(db.Model):
    __tablename__ = "student_leaks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    month = db.Column(SQLAlchemyEnum(MonthEnum), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.Text, nullable=True)  # Permitir NULL para quando só há melhorias
    improvements = db.Column(db.Text, nullable=True)  # Campo para melhorias sugeridas
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relacionamentos removidos para evitar problemas na exclusão

    # Constraint única para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('student_id', 'month', 'year', name='unique_student_leak_month_year'),)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else None,
            'month': self.month.value if self.month else None,
            'year': self.year,
            'image_url': self.image_url,
            'improvements': self.improvements,
            'uploaded_by': self.uploaded_by,
            'uploaded_by_name': self.admin.name if self.admin else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

