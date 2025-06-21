#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar problemas de token
"""

import jwt
import sys
from datetime import datetime, timedelta

def debug_token(token_string, secret_key):
    print(f"🔍 DEBUGANDO TOKEN")
    print("=" * 60)
    print(f"Token: {token_string[:50]}...")
    print(f"Secret Key: {secret_key}")
    print()
    
    try:
        # Tentar decodificar sem verificar expiração
        payload_no_verify = jwt.decode(token_string, secret_key, algorithms=['HS256'], options={"verify_exp": False})
        print("✅ TOKEN DECODIFICADO (sem verificar expiração):")
        print(f"   User ID: {payload_no_verify.get('user_id')}")
        print(f"   User Type: {payload_no_verify.get('user_type')}")
        print(f"   Issued At: {datetime.fromtimestamp(payload_no_verify.get('iat', 0))}")
        print(f"   Expires At: {datetime.fromtimestamp(payload_no_verify.get('exp', 0))}")
        print(f"   Agora: {datetime.utcnow()}")
        
        # Verificar se expirou
        exp_time = datetime.fromtimestamp(payload_no_verify.get('exp', 0))
        now = datetime.utcnow()
        
        if exp_time < now:
            print(f"❌ TOKEN EXPIRADO! Expirou em {exp_time}, agora são {now}")
            time_diff = now - exp_time
            print(f"   Expirou há: {time_diff}")
        else:
            print(f"✅ TOKEN VÁLIDO! Expira em {exp_time}")
            time_diff = exp_time - now
            print(f"   Expira em: {time_diff}")
        
        print()
        
        # Tentar decodificar com verificação completa
        try:
            payload = jwt.decode(token_string, secret_key, algorithms=['HS256'])
            print("✅ TOKEN VÁLIDO COM VERIFICAÇÃO COMPLETA")
            return True
        except jwt.ExpiredSignatureError:
            print("❌ TOKEN EXPIRADO (ExpiredSignatureError)")
            return False
        except jwt.InvalidTokenError as e:
            print(f"❌ TOKEN INVÁLIDO (InvalidTokenError): {e}")
            return False
            
    except Exception as e:
        print(f"❌ ERRO AO DECODIFICAR TOKEN: {e}")
        return False

def generate_new_token(user_id, user_type, secret_key):
    """Gerar um novo token válido"""
    print(f"\n🔧 GERANDO NOVO TOKEN")
    print("=" * 60)
    
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    
    new_token = jwt.encode(payload, secret_key, algorithm='HS256')
    print(f"✅ NOVO TOKEN GERADO:")
    print(f"   Token: {new_token}")
    print(f"   User ID: {user_id}")
    print(f"   User Type: {user_type}")
    print(f"   Expira em: {datetime.utcnow() + timedelta(hours=24)}")
    
    return new_token

if __name__ == "__main__":
    # Secret key do .env
    secret_key = "bf591012fc973e95d4aef904bda3fb9c"
    
    if len(sys.argv) > 1:
        token = sys.argv[1]
        debug_token(token, secret_key)
    else:
        print("❌ Forneça um token como argumento")
        print("Exemplo: python debug_token.py 'seu_token_aqui'")
        print()
        print("🔧 Gerando token de exemplo para user_id=1 (admin):")
        generate_new_token(1, 'admin', secret_key)
