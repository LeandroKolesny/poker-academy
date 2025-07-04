# src/routes/favorites_routes.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app
from src.models import db, Favorites, Classes
from src.auth import token_required

favorites_bp = Blueprint("favorites_bp", __name__)

# Rota para listar favoritos do usuário
@favorites_bp.route("/api/favorites", methods=["GET"])
@token_required
def get_user_favorites(current_user):
    try:
        # Buscar favoritos do usuário com join nas classes
        favorites = db.session.query(Favorites, Classes).join(
            Classes, Favorites.class_id == Classes.id
        ).filter(Favorites.user_id == current_user.id).all()
        
        result = []
        for favorite, class_obj in favorites:
            result.append(class_obj.to_dict())
        
        return jsonify(result), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar favoritos: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar favoritos"), 500

# Rota para adicionar aula aos favoritos
@favorites_bp.route("/api/favorites/<int:class_id>", methods=["POST"])
@token_required
def add_to_favorites(current_user, class_id):
    try:
        # Verificar se a aula existe
        class_obj = Classes.query.get(class_id)
        if not class_obj:
            return jsonify(error="Aula não encontrada"), 404
        
        # Verificar se já está nos favoritos
        existing_favorite = Favorites.query.filter_by(
            user_id=current_user.id,
            class_id=class_id
        ).first()
        
        if existing_favorite:
            return jsonify(error="Aula já está nos favoritos"), 409
        
        # Adicionar aos favoritos
        new_favorite = Favorites(
            user_id=current_user.id,
            class_id=class_id
        )
        
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify(message="Aula adicionada aos favoritos"), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao adicionar favorito: {e}", exc_info=True)
        return jsonify(error="Erro ao adicionar aos favoritos"), 500

# Rota para remover aula dos favoritos
@favorites_bp.route("/api/favorites/<int:class_id>", methods=["DELETE"])
@token_required
def remove_from_favorites(current_user, class_id):
    try:
        favorite = Favorites.query.filter_by(
            user_id=current_user.id,
            class_id=class_id
        ).first()
        
        if not favorite:
            return jsonify(error="Aula não está nos favoritos"), 404
        
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify(message="Aula removida dos favoritos"), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao remover favorito: {e}", exc_info=True)
        return jsonify(error="Erro ao remover dos favoritos"), 500

# Rota para verificar se aula está nos favoritos
@favorites_bp.route("/api/favorites/<int:class_id>/check", methods=["GET"])
@token_required
def check_favorite_status(current_user, class_id):
    try:
        favorite = Favorites.query.filter_by(
            user_id=current_user.id,
            class_id=class_id
        ).first()
        
        return jsonify({"is_favorite": favorite is not None}), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao verificar favorito: {e}", exc_info=True)
        return jsonify(error="Erro ao verificar status do favorito"), 500
