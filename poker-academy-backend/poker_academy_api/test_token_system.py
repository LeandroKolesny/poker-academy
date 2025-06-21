#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar o sistema de tokens corrigido
"""

import jwt
import requests
import json
from datetime import datetime, timedelta

def test_token_system():
    """Testar todo o sistema de tokens"""
    print("🧪 TESTANDO SISTEMA DE TOKENS CORRIGIDO")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    secret_key = "bf591012fc973e95d4aef904bda3fb9c"
    
    # 1. Testar login
    print("1️⃣ TESTANDO LOGIN...")
    login_data = {
        "email": "student@pokeracademy.com",
        "password": "student"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ Login bem-sucedido!")
            print(f"   Token: {token[:50]}...")
            
            # 2. Testar verificação de token
            print("\n2️⃣ TESTANDO VERIFICAÇÃO DE TOKEN...")
            headers = {"Authorization": f"Bearer {token}"}
            verify_response = requests.get(f"{base_url}/api/auth/verify", headers=headers)
            
            if verify_response.status_code == 200:
                user_data = verify_response.json()
                print(f"✅ Token válido!")
                print(f"   Usuário: {user_data['user']['name']}")
                print(f"   Email: {user_data['user']['email']}")
                
                # 3. Testar alteração de senha
                print("\n3️⃣ TESTANDO ALTERAÇÃO DE SENHA...")
                change_password_data = {
                    "current_password": "student",
                    "new_password": "student123"
                }
                
                change_response = requests.put(
                    f"{base_url}/api/auth/change-password", 
                    json=change_password_data,
                    headers=headers
                )
                
                if change_response.status_code == 200:
                    print("✅ Alteração de senha bem-sucedida!")
                    
                    # 4. Reverter senha para o original
                    print("\n4️⃣ REVERTENDO SENHA...")
                    revert_data = {
                        "current_password": "student123",
                        "new_password": "student"
                    }
                    
                    revert_response = requests.put(
                        f"{base_url}/api/auth/change-password", 
                        json=revert_data,
                        headers=headers
                    )
                    
                    if revert_response.status_code == 200:
                        print("✅ Senha revertida com sucesso!")
                    else:
                        print(f"❌ Erro ao reverter senha: {revert_response.text}")
                        
                else:
                    print(f"❌ Erro na alteração de senha: {change_response.text}")
                    
            else:
                print(f"❌ Erro na verificação do token: {verify_response.text}")
                
        else:
            print(f"❌ Erro no login: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
    
    # 5. Testar token expirado
    print("\n5️⃣ TESTANDO TOKEN EXPIRADO...")
    expired_payload = {
        'user_id': 12,
        'user_type': 'student',
        'exp': datetime.utcnow() - timedelta(hours=1),  # Expirado há 1 hora
        'iat': datetime.utcnow() - timedelta(hours=2)
    }
    
    expired_token = jwt.encode(expired_payload, secret_key, algorithm='HS256')
    expired_headers = {"Authorization": f"Bearer {expired_token}"}
    
    try:
        expired_response = requests.get(f"{base_url}/api/auth/verify", headers=expired_headers)
        if expired_response.status_code == 401:
            print("✅ Token expirado rejeitado corretamente!")
        else:
            print(f"❌ Token expirado aceito incorretamente: {expired_response.text}")
    except Exception as e:
        print(f"❌ Erro ao testar token expirado: {e}")
    
    print("\n🎯 TESTE CONCLUÍDO!")
    print("=" * 60)
    print("📋 PRÓXIMOS PASSOS:")
    print("1. Faça login no frontend")
    print("2. Tente alterar a senha")
    print("3. O sistema deve funcionar automaticamente agora!")

if __name__ == "__main__":
    test_token_system()
