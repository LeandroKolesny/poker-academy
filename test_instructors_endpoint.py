#!/usr/bin/env python3
"""
Script para testar o endpoint de instrutores
"""

import requests
import json

BASE_URL = "https://cardroomgrinders.com.br/api"
USERNAME = "admin"
PASSWORD = "admin123"

def login():
    """Fazer login e retornar token"""
    print("🔐 Fazendo login...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": USERNAME, "password": PASSWORD},
        verify=False
    )
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token') or data.get('token')
        print(f"✅ Login bem-sucedido! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Erro ao fazer login: {response.status_code}")
        print(f"Resposta: {response.text}")
        return None

def test_instructors(token):
    """Testar endpoint de instrutores"""
    print("\n📝 Testando /api/instructors...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/instructors",
            headers=headers,
            verify=False
        )
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Sucesso!")
            print(f"Dados: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"\n❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def main():
    """Main"""
    
    # Desabilitar SSL warning
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    token = login()
    if not token:
        return
    
    test_instructors(token)

if __name__ == "__main__":
    main()

