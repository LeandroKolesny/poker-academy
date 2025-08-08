# src/routes/password_reset_routes.py
import os
import base64
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from src.models import db, Users
from src.password_reset_model import PasswordResetToken
from src.auth import AuthService
from src.email_service import EmailService

password_reset_bp = Blueprint('password_reset', __name__)

@password_reset_bp.route("/api/auth/forgot-password", methods=["POST"])
def forgot_password():
    """Endpoint para solicitar recuperação de senha"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Dados não fornecidos"}), 400
        
        email = data.get('email')
        if not email:
            return jsonify({"success": False, "message": "Email é obrigatório"}), 400
        
        # Buscar usuário pelo email
        user = Users.query.filter_by(email=email).first()
        if not user:
            # Por segurança, sempre retornar sucesso mesmo se email não existir
            return jsonify({
                "success": True, 
                "message": "Se o email existir em nossa base, você receberá um link de recuperação"
            }), 200
        
        # Gerar token de reset
        token = EmailService.generate_reset_token(user.id)
        if not token:
            return jsonify({"success": False, "message": "Erro ao gerar token de recuperação"}), 500
        
        # Enviar email
        email_sent = EmailService.send_password_reset_email(user.email, token)
        if not email_sent:
            return jsonify({"success": False, "message": "Erro ao enviar email"}), 500
        
        print(f"✅ Token de reset gerado para {user.email}: {token}")
        
        return jsonify({
            "success": True,
            "message": "Email de recuperação enviado com sucesso"
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro em forgot_password: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Erro interno do servidor"}), 500

@password_reset_bp.route("/api/auth/validate-reset-token", methods=["GET"])
def validate_reset_token():
    """Endpoint para validar token de reset"""
    try:
        token = request.args.get('token')
        if not token:
            return jsonify({"valid": False, "message": "Token não fornecido"}), 400
        
        # Verificar token
        reset_token = EmailService.verify_reset_token(token)
        if not reset_token:
            return jsonify({"valid": False, "message": "Token inválido ou expirado"}), 400
        
        return jsonify({
            "valid": True,
            "message": "Token válido"
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro em validate_reset_token: {e}", exc_info=True)
        return jsonify({"valid": False, "message": "Erro interno do servidor"}), 500

@password_reset_bp.route("/api/auth/reset-password", methods=["POST"])
def reset_password():
    """Endpoint para redefinir senha"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Dados não fornecidos"}), 400
        
        token = data.get('token')
        new_password = data.get('password')
        
        if not token or not new_password:
            return jsonify({"success": False, "message": "Token e senha são obrigatórios"}), 400
        
        if len(new_password) < 6:
            return jsonify({"success": False, "message": "Senha deve ter pelo menos 6 caracteres"}), 400
        
        # Verificar token
        reset_token = EmailService.verify_reset_token(token)
        if not reset_token:
            return jsonify({"success": False, "message": "Token inválido ou expirado"}), 400
        
        # Buscar usuário
        user = Users.query.get(reset_token.user_id)
        if not user:
            return jsonify({"success": False, "message": "Usuário não encontrado"}), 404
        
        # Atualizar senha
        user.password_hash = AuthService.hash_password(new_password)
        
        # Marcar token como usado
        EmailService.mark_token_as_used(token)
        
        # Salvar mudanças
        db.session.commit()
        
        print(f"✅ Senha redefinida para usuário: {user.email}")
        
        return jsonify({
            "success": True,
            "message": "Senha redefinida com sucesso"
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro em reset_password: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"success": False, "message": "Erro interno do servidor"}), 500
