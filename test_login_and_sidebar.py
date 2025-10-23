#!/usr/bin/env python3
"""
Script para testar login e verificar se a aba aparece
"""
import requests
import json

# Desabilitar warnings de SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://cardroomgrinders.com.br/api"
STUDENT_USERNAME = "leandrokoles"
STUDENT_PASSWORD = "leandrokoles123456"

print("=" * 60)
print("🧪 TESTE DE LOGIN E SIDEBAR")
print("=" * 60)

# 1. Login
print("\n1️⃣  Fazendo login...")
login_response = requests.post(
    f"{API_URL}/auth/login",
    json={"username": STUDENT_USERNAME, "password": STUDENT_PASSWORD},
    verify=False
)

print(f"Status: {login_response.status_code}")
print(f"Response: {login_response.json()}")

if login_response.status_code != 200:
    print(f"❌ Erro no login!")
    exit(1)

token = login_response.json()['token']
user_data = login_response.json()['user']
print(f"✅ Login bem-sucedido!")
print(f"Token: {token[:30]}...")
print(f"Usuário: {user_data['name']}")
print(f"Tipo: {user_data['type']}")
print(f"ID: {user_data['id']}")

headers = {"Authorization": f"Bearer {token}"}

# 3. Testar rota de database
print("\n3️⃣  Testando rota GET /api/student/database...")
db_response = requests.get(
    f"{API_URL}/student/database?year=2025",
    headers=headers,
    verify=False
)

print(f"Status: {db_response.status_code}")
print(f"Response: {db_response.json()}")

if db_response.status_code == 200:
    print("✅ Rota de database funcionando!")
else:
    print("❌ Erro na rota de database!")

print("\n" + "=" * 60)
print("✅ TESTES CONCLUÍDOS!")
print("=" * 60)

