#!/usr/bin/env python3
"""
Script para testar a correção de partições
"""

import requests
import json
import time

BASE_URL = "https://cardroomgrinders.com.br"
API_BASE_URL = "https://cardroomgrinders.com.br/api"

def test_partition_fix():
    """Testa se a correção de partições funcionou"""
    
    print("🧪 TESTANDO CORREÇÃO DE PARTIÇÕES\n")
    
    try:
        # 1. Login
        print("1️⃣ Fazendo login...")
        login_response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": "admin", "password": "admin123"},
            verify=False
        )
        
        if login_response.status_code != 200:
            print(f"❌ Erro no login: {login_response.status_code}")
            print(login_response.text)
            return False
        
        token = login_response.json().get('token')
        print(f"✅ Login bem-sucedido! Token: {token[:20]}...")
        
        # 2. Buscar partições
        print("\n2️⃣ Buscando partições...")
        headers = {"Authorization": f"Bearer {token}"}
        
        particoes_response = requests.get(
            f"{API_BASE_URL}/particoes",
            headers=headers,
            verify=False
        )
        
        if particoes_response.status_code != 200:
            print(f"❌ Erro ao buscar partições: {particoes_response.status_code}")
            return False
        
        particoes = particoes_response.json()
        print(f"✅ Partições carregadas: {len(particoes)} partições")
        
        for p in particoes:
            print(f"   - ID: {p['id']} (tipo: {type(p['id']).__name__}), Nome: {p['nome']}")
        
        # 3. Verificar tipos
        print("\n3️⃣ Verificando tipos de dados...")
        all_ids_are_numbers = all(isinstance(p['id'], int) for p in particoes)
        
        if all_ids_are_numbers:
            print("✅ Todos os IDs são números (correto!)")
        else:
            print("❌ Alguns IDs não são números")
            return False
        
        # 4. Criar novo aluno (teste)
        print("\n4️⃣ Testando criação de aluno com partição...")
        
        if len(particoes) > 0:
            particao_id = particoes[0]['id']
            
            new_student = {
                "name": "Teste Partição",
                "username": f"teste_particao_{int(time.time())}",
                "email": f"teste_{int(time.time())}@test.com",
                "password": "test123456",
                "particao_id": particao_id
            }
            
            create_response = requests.post(
                f"{API_BASE_URL}/users",
                json=new_student,
                headers=headers,
                verify=False
            )
            
            if create_response.status_code in [200, 201]:
                print(f"✅ Aluno criado com sucesso!")
                student_data = create_response.json()
                print(f"   - ID: {student_data.get('id')}")
                print(f"   - Nome: {student_data.get('name')}")
                print(f"   - Partição ID: {student_data.get('particao_id')}")
            else:
                print(f"⚠️  Erro ao criar aluno: {create_response.status_code}")
                print(create_response.text)
        
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_partition_fix()

