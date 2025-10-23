#!/usr/bin/env python3
"""
Script para testar encoding de todos os endpoints da API
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
        return None

def test_endpoint(token, endpoint, name):
    """Testar um endpoint e verificar encoding"""
    print(f"\n📝 Testando {name}...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificar se há problemas de encoding
            json_str = json.dumps(data, ensure_ascii=False)
            
            if 'Ã' in json_str or 'Â' in json_str:
                print(f"  ❌ Problema de encoding detectado!")
                print(f"  Amostra: {json_str[:200]}")
            else:
                print(f"  ✅ Encoding OK!")
                
                # Mostrar amostra de dados
                if isinstance(data, list) and len(data) > 0:
                    print(f"  Exemplo: {json.dumps(data[0], ensure_ascii=False)[:150]}")
                elif isinstance(data, dict):
                    print(f"  Exemplo: {json.dumps(data, ensure_ascii=False)[:150]}")
        else:
            print(f"  ⚠️ Status: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Erro: {str(e)}")

def main():
    """Main"""
    
    # Desabilitar SSL warning
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    token = login()
    if not token:
        return
    
    # Testar endpoints
    endpoints = [
        ("/particoes", "Partições"),
        ("/classes", "Classes"),
        ("/users", "Usuários"),
        ("/instructors", "Instrutores"),
    ]
    
    for endpoint, name in endpoints:
        test_endpoint(token, endpoint, name)
    
    print("\n✅ TESTE COMPLETO!")

if __name__ == "__main__":
    main()

