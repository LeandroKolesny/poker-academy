#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir problema de token expirado
"""

import jwt
import sys
import os
from datetime import datetime, timedelta

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from auth import AuthService

def generate_fresh_token(user_id=2, user_type='student'):
    """Gerar um token fresco para teste"""
    print(f"🔧 GERANDO TOKEN FRESCO PARA TESTE")
    print("=" * 60)
    
    # Secret key do .env
    secret_key = "bf591012fc973e95d4aef904bda3fb9c"
    
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    print(f"✅ TOKEN GERADO:")
    print(f"   User ID: {user_id}")
    print(f"   User Type: {user_type}")
    print(f"   Token: {token}")
    print(f"   Expira em: {datetime.utcnow() + timedelta(hours=24)}")
    print()
    print("📋 INSTRUÇÕES:")
    print("1. Copie o token acima")
    print("2. Abra o DevTools do navegador (F12)")
    print("3. Vá para a aba Application > Local Storage")
    print("4. Encontre a chave 'token' e substitua o valor pelo token acima")
    print("5. Recarregue a página e tente alterar a senha novamente")
    
    return token

def test_token_validation(token):
    """Testar se um token é válido"""
    print(f"🔍 TESTANDO VALIDAÇÃO DO TOKEN")
    print("=" * 60)
    
    secret_key = "bf591012fc973e95d4aef904bda3fb9c"
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        print("✅ TOKEN VÁLIDO!")
        print(f"   User ID: {payload.get('user_id')}")
        print(f"   User Type: {payload.get('user_type')}")
        print(f"   Expira em: {datetime.fromtimestamp(payload.get('exp'))}")
        return True
    except jwt.ExpiredSignatureError:
        print("❌ TOKEN EXPIRADO!")
        return False
    except jwt.InvalidTokenError as e:
        print(f"❌ TOKEN INVÁLIDO: {e}")
        return False

if __name__ == "__main__":
    print("🚀 CORREÇÃO DE PROBLEMA DE TOKEN")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Testar um token específico
            if len(sys.argv) > 2:
                test_token_validation(sys.argv[2])
            else:
                print("❌ Forneça um token para testar")
        elif sys.argv[1] == "admin":
            # Gerar token para admin
            generate_fresh_token(1, 'admin')
        else:
            # Testar token fornecido
            test_token_validation(sys.argv[1])
    else:
        # Gerar token para estudante por padrão
        generate_fresh_token(2, 'student')
