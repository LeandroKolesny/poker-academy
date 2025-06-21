#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar token para estudante específico
"""

import jwt
from datetime import datetime, timedelta

def generate_student_token():
    """Gerar token para o estudante ID 12"""
    print(f"🔧 GERANDO TOKEN PARA ESTUDANTE")
    print("=" * 60)
    
    # Secret key do .env
    secret_key = "bf591012fc973e95d4aef904bda3fb9c"
    
    # ID 12 = Student Test
    payload = {
        'user_id': 12,
        'user_type': 'student',
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    print(f"✅ TOKEN GERADO PARA STUDENT TEST:")
    print(f"   User ID: 12")
    print(f"   User Type: student")
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

if __name__ == "__main__":
    generate_student_token()
