# src/email_service.py
import os
import base64
import json
import requests
from datetime import datetime, timedelta

from src.models import db, Users
from src.password_reset_model import PasswordResetToken

class EmailService:
    
    @staticmethod
    def generate_reset_token(user_id):
        """Gerar token de reset de senha"""
        try:
            # Invalidar tokens existentes do usuário
            existing_tokens = PasswordResetToken.query.filter_by(user_id=user_id, used=False).all()
            for token in existing_tokens:
                token.used = True
            
            # Gerar novo token
            token = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")
            expires_at = datetime.utcnow() + timedelta(hours=1)  # Expira em 1 hora
            
            # Salvar no banco
            reset_token = PasswordResetToken(
                user_id=user_id,
                token=token,
                expires_at=expires_at
            )
            
            db.session.add(reset_token)
            db.session.commit()
            
            return token
            
        except Exception as e:
            print(f"Erro ao gerar token: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def verify_reset_token(token):
        """Verificar se token é válido"""
        try:
            reset_token = PasswordResetToken.query.filter_by(
                token=token, 
                used=False
            ).first()
            
            if not reset_token:
                return None
                
            # Verificar se não expirou
            if datetime.utcnow() > reset_token.expires_at:
                return None
                
            return reset_token
            
        except Exception as e:
            print(f"Erro ao verificar token: {e}")
            return None
    
    @staticmethod
    def mark_token_as_used(token):
        """Marcar token como usado"""
        try:
            reset_token = PasswordResetToken.query.filter_by(token=token).first()
            if reset_token:
                reset_token.used = True
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Erro ao marcar token como usado: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def send_password_reset_email(user_email, reset_token, user_name=None):
        """Enviar email de recuperação de senha via Brevo"""
        try:
            # Se não foi fornecido nome, usar 'Jogador' como padrão
            display_name = user_name if user_name else "Jogador"
            
            # URL de reset
            reset_url = f"https://cardroomgrinders.com.br/reset-password?token={reset_token}"
            
            # Template HTML do email - CORRIGIDO
            html_content = f"""
<\!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperação de Senha - CardRoom Grinders</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: 'Arial', sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 40px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; max-width: 600px;">
                    
                    <\!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 60px 40px; text-align: center;">
                            <div style="background: rgba(255,255,255,0.1); border-radius: 50%; width: 80px; height: 80px; margin: 0 auto 25px; display: flex; align-items: center; justify-content: center;">
                                <span style="font-size: 40px;">🔐</span>
                            </div>
                            <h1 style="color: #feca57; margin: 0 0 10px 0; font-size: 32px; font-weight: bold;">
                                Recuperação de Senha
                            </h1>
                            <div style="color: #feca57; font-size: 22px; font-weight: bold; letter-spacing: 2px;">
                                CARDROOM GRINDERS
                            </div>
                        </td>
                    </tr>
                    
                    <\!-- Content -->
                    <tr>
                        <td style="padding: 50px 40px;">
                            <h2 style="color: #2c3e50; text-align: center; margin: 0 0 30px 0; font-size: 26px;">
                                Olá, {display_name}\! 👋
                            </h2>
                            
                            <p style="color: #555; font-size: 16px; line-height: 1.6; text-align: center; margin-bottom: 30px;">
                                Recebemos uma solicitação para redefinir a senha da sua conta no <strong>CardRoom Grinders</strong>.
                            </p>
                            
                            <\!-- Alert Box -->
                            <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin: 30px 0; text-align: center;">
                                <span style="font-size: 24px; margin-bottom: 10px; display: block;">⏰</span>
                                <p style="color: #856404; margin: 0; font-weight: bold;">
                                    Este link expira em 1 hora por motivos de segurança
                                </p>
                            </div>
                            
                            <\!-- Button -->
                            <div style="text-align: center; margin: 40px 0;">
                                <a href="{reset_url}"
                                   style="display: inline-block;
                                          background-color: #ff6b6b;
                                          color: #ffffff;
                                          text-decoration: none;
                                          padding: 20px 50px;
                                          border-radius: 50px;
                                          font-weight: bold;
                                          font-size: 18px;
                                          text-transform: uppercase;
                                          letter-spacing: 1px;
                                          box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);">
                                    🔑 Redefinir Minha Senha
                                </a>
                            </div>
                            
                            <p style="color: #777; font-size: 14px; text-align: center; margin-top: 30px;">
                                Se você não solicitou esta recuperação, pode ignorar este email com segurança.
                            </p>
                        </td>
                    </tr>
                    
                    <\!-- Alternative Link -->
                    <tr>
                        <td style="background: #f8f9fa; padding: 30px 40px; border-top: 1px solid #dee2e6;">
                            <h4 style="color: #495057; margin: 0 0 15px 0; text-align: center;">
                                Problemas com o botão? 🤔
                            </h4>
                            <p style="color: #6c757d; font-size: 14px; text-align: center; margin-bottom: 15px;">
                                Copie e cole este link no seu navegador:
                            </p>
                            <div style="background: #ffffff; border: 2px dashed #dee2e6; border-radius: 8px; padding: 15px; text-align: center;">
                                <a href="{reset_url}" style="color: #ff6b6b; font-size: 12px; word-break: break-all; text-decoration: none;">
                                    {reset_url}
                                </a>
                            </div>
                        </td>
                    </tr>
                    
                    <\!-- Footer -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); padding: 40px; text-align: center;">
                            <div style="margin-bottom: 20px;">
                                <span style="color: #bdc3c7; font-size: 24px; margin: 0 8px;">♠️</span>
                                <span style="color: #bdc3c7; font-size: 24px; margin: 0 8px;">♥️</span>
                                <span style="color: #bdc3c7; font-size: 24px; margin: 0 8px;">♣️</span>
                                <span style="color: #bdc3c7; font-size: 24px; margin: 0 8px;">♦️</span>
                            </div>
                            
                            <div style="color: #feca57; font-size: 18px; font-weight: bold; margin-bottom: 15px;">
                                CARDROOM GRINDERS
                            </div>
                            
                            <p style="color: #95a5a6; font-size: 12px; margin: 0;">
                                © 2025 CardRoom Grinders. Todos os direitos reservados.<br>
                                Este é um email automático, não responda a esta mensagem.
                            </p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
            """
            
            # Tentar enviar via Brevo
            brevo_api_key = os.getenv("BREVO_API_KEY")
            if brevo_api_key:
                try:
                    url = "https://api.brevo.com/v3/smtp/email"
                    headers = {
                        "accept": "application/json",
                        "api-key": brevo_api_key,
                        "content-type": "application/json"
                    }
                    
                    payload = {
                        "sender": {
                            "name": "CardRoom Grinders",
                            "email": "dojopokerteam@gmail.com"
                        },
                        "to": [
                            {
                                "email": user_email,
                                "name": display_name
                            }
                        ],
                        "subject": "🔐 Recuperação de Senha - CardRoom Grinders",
                        "htmlContent": html_content
                    }
                    
                    response = requests.post(url, json=payload, headers=headers)
                    
                    if response.status_code == 201:
                        print(f"✅ Email enviado via Brevo para: {user_email}")
                        print(f"📧 Message ID: {response.json().get('messageId')}")
                        return True
                    else:
                        print(f"❌ Erro Brevo: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    print(f"❌ Erro ao enviar via Brevo: {e}")
            
            # Fallback: salvar em log
            log_file = "/tmp/password_reset_emails.log"
            separator = "=" * 50
            
            with open(log_file, "a") as f:
                f.write(f"\n{separator}\n")
                f.write(f"Data: {datetime.now()}\n")
                f.write(f"Para: {user_email}\n")
                f.write(f"Nome: {display_name}\n")
                f.write(f"Token: {reset_token}\n")
                f.write(f"Link: {reset_url}\n")
                f.write(f"{separator}\n")
            
            print(f"📝 Email salvo em log: {log_file}")
            print(f"🔗 Link de reset para {display_name} ({user_email}): {reset_url}")
            return True
            
        except Exception as e:
            print(f"❌ Erro geral ao enviar email: {e}")
            return False
