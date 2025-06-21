#!/usr/bin/env python3
"""
Script para testar as APIs do sistema
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_particoes():
    """Testa a API de partições"""
    print("=== TESTANDO API DE PARTIÇÕES ===")
    
    try:
        response = requests.get(f"{BASE_URL}/api/particoes")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Partições encontradas: {len(data)}")
            for particao in data:
                print(f"  - ID: {particao['id']}, Nome: {particao['nome']}, Ativa: {particao['ativa']}")
        else:
            print(f"Erro: {response.text}")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

def test_login():
    """Testa login e retorna token"""
    print("\n=== TESTANDO LOGIN ===")
    
    login_data = {
        "email": "Lekolesny@hotmail.com",  # Email do admin principal
        "password": "123456"  # Senha padrão
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Resposta do login: {data}")  # Debug
            token = data.get('access_token') or data.get('token')
            print(f"Login realizado com sucesso!")
            print(f"Token: {token[:50]}..." if token else "Token não encontrado")
            return token
        else:
            print(f"Erro no login: {response.text}")
            return None
            
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

def test_create_student(token):
    """Testa criação de estudante"""
    print("\n=== TESTANDO CRIAÇÃO DE ESTUDANTE ===")
    
    if not token:
        print("Token não disponível, pulando teste")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    student_data = {
        "name": "Teste Aluno",
        "username": "teste_aluno",
        "email": "teste@teste.com",
        "password": "123456",
        "particao_id": 1  # ID da partição Dojo
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/users", json=student_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"Estudante criado com sucesso!")
            print(f"ID: {data.get('id')}, Nome: {data.get('name')}")
        else:
            print(f"Erro na criação: {response.text}")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

def test_get_students(token):
    """Testa listagem de estudantes"""
    print("\n=== TESTANDO LISTAGEM DE ESTUDANTES ===")
    
    if not token:
        print("Token não disponível, pulando teste")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/users", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Estudantes encontrados: {len(data)}")
            for student in data:
                print(f"  - ID: {student['id']}, Nome: {student['name']}, Partição: {student.get('particao_nome', 'N/A')}")
        else:
            print(f"Erro na listagem: {response.text}")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

def main():
    """Função principal"""
    print("🧪 TESTE DAS APIs DO POKER ACADEMY")
    print("=" * 50)
    
    # Teste 1: Partições
    test_particoes()
    
    # Teste 2: Login
    token = test_login()
    
    # Teste 3: Listagem de estudantes
    test_get_students(token)
    
    # Teste 4: Criação de estudante
    test_create_student(token)
    
    # Teste 5: Listagem novamente para ver o novo estudante
    test_get_students(token)
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Testes interrompidos pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
