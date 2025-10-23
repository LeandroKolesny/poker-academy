# src/routes/particao_routes.py
import sys
import os

# Adiciona o diretório pai de 'src' (ou seja, 'poker_academy_api') ao sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app
from src.models import db, Particoes
from src.auth import AuthService, admin_required

particao_bp = Blueprint("particao_bp", __name__)

# Rota para listar todas as partições ativas (para dropdown)
@particao_bp.route("/api/particoes", methods=["GET"])
def get_particoes():
    """Lista todas as partições ativas"""
    try:
        particoes = Particoes.query.filter_by(ativa=True).order_by(Particoes.nome).all()
        result = [particao.to_dict() for particao in particoes]
        return jsonify({'data': result}), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar partições: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar partições."), 500

# Rota para listar todas as partições (incluindo inativas) - apenas admin
@particao_bp.route("/api/particoes/all", methods=["GET"])
@admin_required
def get_all_particoes(current_user):
    """Lista todas as partições (incluindo inativas) - apenas admin"""
    try:
        particoes = Particoes.query.order_by(Particoes.nome).all()
        result = [particao.to_dict() for particao in particoes]
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar todas as partições: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar partições."), 500

# Rota para criar nova partição - apenas admin
@particao_bp.route("/api/particoes", methods=["POST"])
@admin_required
def create_particao(current_user):
    """Cria nova partição - apenas admin"""
    data = request.get_json()
    if not data:
        return jsonify(error="Dados não fornecidos"), 400

    # Campos obrigatórios
    required_fields = ["nome"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify(error=f"Campo obrigatório ausente ou vazio: {field}"), 400

    # Verificar se nome já existe
    if Particoes.query.filter_by(nome=data["nome"]).first():
        return jsonify(error="Nome da partição já existe."), 409

    try:
        nova_particao = Particoes(
            nome=data["nome"],
            descricao=data.get("descricao", ""),
            ativa=data.get("ativa", True)
        )
        db.session.add(nova_particao)
        db.session.commit()
        return jsonify(nova_particao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar partição: {e}", exc_info=True)
        return jsonify(error=f"Erro ao criar nova partição: {str(e)}"), 500

# Rota para atualizar partição - apenas admin
@particao_bp.route("/api/particoes/<int:particao_id>", methods=["PUT"])
@admin_required
def update_particao(current_user, particao_id):
    """Atualiza partição existente - apenas admin"""
    data = request.get_json()
    if not data:
        return jsonify(error="Dados não fornecidos"), 400

    particao = Particoes.query.get(particao_id)
    if not particao:
        return jsonify(error="Partição não encontrada"), 404

    try:
        # Atualizar nome se fornecido e diferente
        if "nome" in data and data["nome"] and data["nome"] != particao.nome:
            if Particoes.query.filter(Particoes.id != particao_id, Particoes.nome == data["nome"]).first():
                return jsonify(error="Nome da partição já existe."), 409
            particao.nome = data["nome"]
        
        # Atualizar descrição se fornecida
        if "descricao" in data:
            particao.descricao = data["descricao"]
        
        # Atualizar status ativo se fornecido
        if "ativa" in data:
            particao.ativa = bool(data["ativa"])
        
        db.session.commit()
        return jsonify(particao.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar partição {particao_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao atualizar partição: {str(e)}"), 500

# Rota para desativar partição (soft delete) - apenas admin
@particao_bp.route("/api/particoes/<int:particao_id>", methods=["DELETE"])
@admin_required
def delete_particao(current_user, particao_id):
    """Desativa partição (soft delete) - apenas admin"""
    particao = Particoes.query.get(particao_id)
    if not particao:
        return jsonify(error="Partição não encontrada"), 404
    
    # Verificar se há usuários usando esta partição
    from src.models import Users
    users_count = Users.query.filter_by(particao_id=particao_id).count()
    
    if users_count > 0:
        return jsonify(error=f"Não é possível desativar esta partição. {users_count} usuário(s) ainda estão vinculados a ela."), 400
    
    try:
        # Soft delete - apenas desativar
        particao.ativa = False
        db.session.commit()
        return jsonify(message="Partição desativada com sucesso"), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao desativar partição {particao_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao desativar partição: {str(e)}"), 500

# Rota para obter uma partição específica
@particao_bp.route("/api/particoes/<int:particao_id>", methods=["GET"])
def get_particao(particao_id):
    """Obtém uma partição específica"""
    try:
        particao = Particoes.query.get(particao_id)
        if not particao:
            return jsonify(error="Partição não encontrada"), 404
        
        return jsonify(particao.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar partição {particao_id}: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar partição."), 500
