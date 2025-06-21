#!/usr/bin/env python3
"""
Script para testar e corrigir datas no banco de dados
"""

import requests
import json

# Configurações da API
API_BASE_URL = "http://localhost:5000"

def test_date_creation():
    """Testa criação de aula com data específica"""
    
    print("🧪 Testando criação de aula com data 17/06/2025...")
    
    # Primeiro fazer login para obter token
    login_data = {
        "email": "admin@pokeracademy.com",
        "password": "admin123"
    }
    
    print("🔐 Fazendo login...")
    login_response = requests.post(f"{API_BASE_URL}/api/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Erro no login: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json().get("access_token")
    print("✅ Login realizado com sucesso!")
    
    # Dados da aula de teste
    class_data = {
        "name": "TESTE DATA CORRETA",
        "instructor": "leandro",
        "date": "2025-06-17",  # Data que queremos testar
        "category": "preflop",
        "video_type": "local",
        "video_path": "teste_data.mp4",
        "priority": 5
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"📤 Enviando dados: {class_data}")
    
    # Criar aula
    create_response = requests.post(f"{API_BASE_URL}/api/classes", json=class_data, headers=headers)
    
    if create_response.status_code != 201:
        print(f"❌ Erro ao criar aula: {create_response.status_code}")
        print(create_response.text)
        return
    
    created_class = create_response.json()
    print(f"✅ Aula criada com ID: {created_class['id']}")
    print(f"📅 Data salva: {created_class['date']}")
    
    # Verificar se a data está correta
    if created_class['date'] == "2025-06-17":
        print("✅ DATA CORRETA! Problema resolvido!")
    else:
        print(f"❌ DATA INCORRETA! Esperado: 2025-06-17, Recebido: {created_class['date']}")
    
    # Buscar todas as aulas para verificar
    print("\n🔍 Buscando todas as aulas...")
    get_response = requests.get(f"{API_BASE_URL}/api/classes", headers=headers)
    
    if get_response.status_code == 200:
        classes = get_response.json()
        print(f"📋 Total de aulas: {len(classes)}")
        
        # Mostrar as últimas 3 aulas
        for cls in classes[-3:]:
            print(f"  - {cls['name']}: {cls['date']}")
    
    # Limpar aula de teste
    print(f"\n🧹 Removendo aula de teste (ID: {created_class['id']})...")
    delete_response = requests.delete(f"{API_BASE_URL}/api/classes/{created_class['id']}", headers=headers)
    
    if delete_response.status_code == 200:
        print("✅ Aula de teste removida!")
    else:
        print(f"⚠️ Não foi possível remover a aula de teste: {delete_response.status_code}")

if __name__ == "__main__":
    test_date_creation()
