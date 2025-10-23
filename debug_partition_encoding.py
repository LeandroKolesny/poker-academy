#!/usr/bin/env python3
"""
Script para debugar o encoding das partições
"""

import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://cardroomgrinders.com.br/api"

def test_partition_encoding():
    """Testa o encoding das partições"""
    
    print("🧪 TESTANDO ENCODING DAS PARTIÇÕES\n")
    
    try:
        # 1. Login
        print("1️⃣ Fazendo login...")
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "admin", "password": "admin123"},
            verify=False
        )
        
        token = login_response.json().get('token')
        print(f"✅ Login bem-sucedido!\n")
        
        # 2. Buscar partições
        print("2️⃣ Buscando partições...")
        headers = {"Authorization": f"Bearer {token}"}
        
        particoes_response = requests.get(
            f"{BASE_URL}/particoes",
            headers=headers,
            verify=False
        )
        
        print(f"Status: {particoes_response.status_code}")
        print(f"Content-Type: {particoes_response.headers.get('Content-Type')}")
        print(f"Encoding: {particoes_response.encoding}\n")
        
        # 3. Analisar resposta
        print("3️⃣ Analisando resposta...")
        particoes = particoes_response.json()
        
        print(f"Número de partições: {len(particoes)}\n")
        
        for p in particoes:
            print(f"Partição ID: {p['id']}")
            print(f"  Nome (raw): {repr(p['nome'])}")
            print(f"  Nome (display): {p['nome']}")
            print(f"  Descrição (raw): {repr(p['descricao'])}")
            print(f"  Descrição (display): {p['descricao']}")
            print()
        
        # 4. Verificar bytes
        print("4️⃣ Verificando bytes...")
        raw_text = particoes_response.text
        print(f"Raw response (primeiros 500 chars):\n{raw_text[:500]}\n")
        
        # 5. Verificar se é problema de encoding
        print("5️⃣ Verificando encoding...")
        for p in particoes:
            nome = p['nome']
            print(f"Nome: {nome}")
            print(f"  Bytes: {nome.encode('utf-8')}")
            print(f"  Decodificado: {nome.encode('utf-8').decode('utf-8')}")
            print()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_partition_encoding()

