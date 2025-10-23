#!/usr/bin/env python3
"""
Script para testar o sistema de verdade
"""
import requests
import json
import time
from urllib.parse import urljoin

# Desabilitar warnings de SSL
requests.packages.urllib3.disable_warnings()

BASE_URL = "https://cardroomgrinders.com.br"
session = requests.Session()
session.verify = False

print("🔌 Testando o sistema...")

# 1. Fazer login
print("\n1️⃣  Fazendo login...")
login_data = {
    "username": "leandrokoles",
    "password": "leandrokoles123456"
}

response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    token = data.get('token')
    print(f"✅ Login bem-sucedido!")
    print(f"Token: {token[:50]}...")
else:
    print(f"❌ Erro no login: {response.text}")
    exit(1)

# 2. Testar a rota de database
print("\n2️⃣  Testando rota /api/student/database...")
headers = {"Authorization": f"Bearer {token}"}
response = session.get(f"{BASE_URL}/api/student/database?year=2025", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

# 3. Verificar o HTML da página
print("\n3️⃣  Verificando HTML da página...")
response = session.get(f"{BASE_URL}/", headers=headers)
print(f"Status: {response.status_code}")

# Procurar por 'monthly-database' no HTML
if 'monthly-database' in response.text:
    print("✅ 'monthly-database' encontrado no HTML")
else:
    print("❌ 'monthly-database' NÃO encontrado no HTML")

# Procurar por '/student/catalog' no HTML
if '/student/catalog' in response.text:
    print("✅ '/student/catalog' encontrado no HTML")
else:
    print("❌ '/student/catalog' NÃO encontrado no HTML")

# Procurar por 'to="catalog"' no HTML
if 'to="catalog"' in response.text:
    print("⚠️  'to=\"catalog\"' encontrado no HTML (caminho relativo)")
else:
    print("✅ Sem 'to=\"catalog\"' (caminhos relativos removidos)")

print("\n✅ Teste concluído!")

