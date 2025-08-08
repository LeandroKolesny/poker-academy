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
            
            # APENAS TEXTO PURO - SEM HTML
            email_text = f"""🔐
Recuperação de Senha
CARDROOM GRINDERS

Olá, {display_name}\! 👋

Recebemos uma solicitação para redefinir a senha da sua conta no CardRoom Grinders.

⏰
Este link expira em 1 hora por motivos de segurança

🔑 Redefinir Minha Senha
{reset_url}

Se você não solicitou esta recuperação, pode ignorar este email com segurança.

Problemas com o botão? 🤔
Copie e cole este link no seu navegador:

{reset_url}

♠️ ♥️ ♣️ ♦️
CARDROOM GRINDERS
© 2025 CardRoom Grinders. Todos os direitos reservados.
Este é um email automático, não responda a esta mensagem."""

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
                        "to": [{"email": user_email, "name": display_name}],
                        "subject": "🔐 Recuperação de Senha - CardRoom Grinders",
                        "textContent": email_text
                    }
                    
                    response = requests.post(url, json=payload, headers=headers)
                    
                    if response.status_code == 201:
                        print(f"✅ Email enviado via Brevo para: {user_email}")
                        print(f"📧 Message ID: {response.json().get(\"messageId\")}")
                        return True
                    else:
                        print(f"❌ Erro Brevo: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    print(f"❌ Erro ao enviar via Brevo: {e}")
            
            return False
            
        except Exception as e:
            print(f"❌ Erro geral ao enviar email: {e}")
            return False
