import os
import base64
import requests
from datetime import datetime, timedelta
from src.models import db, Users
from src.password_reset_model import PasswordResetToken

class EmailService:
    
    @staticmethod
    def generate_reset_token(user_id):
        try:
            existing_tokens = PasswordResetToken.query.filter_by(user_id=user_id, used=False).all()
            for token in existing_tokens:
                token.used = True
            
            token = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
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
        try:
            reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()
            if not reset_token:
                return None
            if datetime.utcnow() > reset_token.expires_at:
                return None
            return reset_token
        except Exception as e:
            print(f"Erro ao verificar token: {e}")
            return None
    
    @staticmethod
    def mark_token_as_used(token):
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
        try:
            display_name = user_name if user_name else "Jogador"
            reset_url = f"https://cardroomgrinders.com.br/reset-password?token={reset_token}"
            
            email_html = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>Recuperação de Senha - CardRoom Grinders</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        
        <div style="background-color: #dc2626; padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 28px; font-weight: bold;">CardRoom Grinders</h1>
            <p style="color: #fecaca; margin: 10px 0 0 0; font-size: 16px;">Recuperação de Senha</p>
        </div>
        
        <div style="padding: 40px 30px;">
            <h2 style="color: #333; margin: 0 0 20px 0; font-size: 24px;">Olá, {display_name}\!</h2>
            
            <p style="color: #666; line-height: 1.6; margin: 0 0 20px 0;">
                Recebemos uma solicitação para redefinir a senha da sua conta no <strong>CardRoom Grinders</strong>.
                Para sua segurança, clique no botão abaixo para criar uma nova senha.
            </p>
            
            <div style="background-color: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 15px; margin: 20px 0;">
                <p style="color: #92400e; margin: 0; font-weight: bold;">
                    ⚠️ Importante: Este link expira em 1 hora por motivos de segurança.
                </p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" style="display: inline-block; background-color: #dc2626; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    🔐 Redefinir Senha
                </a>
            </div>
            
            <p style="color: #999; text-align: center; font-size: 14px; margin: 20px 0;">
                Se você não solicitou esta recuperação, pode ignorar este email com segurança.<br>
                Sua senha atual permanecerá inalterada.
            </p>
            
            <div style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <p style="color: #374151; margin: 0 0 10px 0; font-weight: bold;">Problemas com o botão?</p>
                <p style="color: #6b7280; margin: 0 0 10px 0; font-size: 13px;">Copie e cole este link no seu navegador:</p>
                <p style="color: #2563eb; margin: 0; font-size: 13px; word-break: break-all;">
                    <a href="{reset_url}" style="color: #2563eb;">{reset_url}</a>
                </p>
            </div>
        </div>
        
        <div style="background-color: #f8fafc; padding: 25px; text-align: center; border-top: 1px solid #e5e7eb;">
            <p style="color: #dc2626; margin: 0 0 10px 0; font-size: 18px;">♠️ ♥️ ♣️ ♦️</p>
            <p style="color: #333; margin: 0 0 10px 0; font-size: 18px; font-weight: bold; letter-spacing: 1px;">CARDROOM GRINDERS</p>
            <p style="color: #6b7280; margin: 0; font-size: 12px;">
                © 2025 CardRoom Grinders. Todos os direitos reservados.<br>
                Este é um email automático, não responda a esta mensagem.
            </p>
        </div>
        
    </div>
</body>
</html>
"""

            email_text = f"""🔐 Recuperação de Senha - CARDROOM GRINDERS

Olá, {display_name}\! 👋

Recebemos uma solicitação para redefinir a senha da sua conta no CardRoom Grinders.

⏰ IMPORTANTE: Este link expira em 1 hora por motivos de segurança.

🔑 Redefinir Minha Senha:
{reset_url}

Se você não solicitou esta recuperação, pode ignorar este email com segurança.

Problemas com o link? Copie e cole no seu navegador:
{reset_url}

♠️ ♥️ ♣️ ♦️
CARDROOM GRINDERS
© 2025 CardRoom Grinders. Todos os direitos reservados.
Este é um email automático, não responda a esta mensagem."""

            brevo_api_key = os.getenv("BREVO_API_KEY")
            if brevo_api_key and brevo_api_key != "your_brevo_api_key_here":
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
                        "to": [{"email": user_email, "name": display_name}],
                        "subject": "🔐 Recuperação de Senha - CardRoom Grinders",
                        "htmlContent": email_html,
                        "textContent": email_text
                    }

                    response = requests.post(url, json=payload, headers=headers)

                    if response.status_code == 201:
                        print(f"✅ Email enviado via Brevo para: {user_email}")
                        message_id = response.json().get("messageId")
                        print(f"📧 Message ID: {message_id}")
                        return True
                    else:
                        print(f"❌ Erro Brevo: {response.status_code} - {response.text}")

                except Exception as e:
                    print(f"❌ Erro ao enviar via Brevo: {e}")
            else:
                print(f"🔧 MODO TESTE: Email de recuperação simulado para {user_email}")
                print(f"🔗 Link de recuperação: {reset_url}")
                print(f"📧 Conteúdo do email:")
                print(email_text)
                print("=" * 50)
                return True

            return False
            
        except Exception as e:
            print(f"❌ Erro geral ao enviar email: {e}")
            return False
