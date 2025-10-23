#!/usr/bin/env python3
"""
Script para testar a navegação real do sistema
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

print("🔌 Testando navegação real do sistema...")

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
else:
    print(f"❌ Erro no login: {response.text}")
    exit(1)

# 2. Testar a rota de database
print("\n2️⃣  Testando rota /api/student/database...")
headers = {"Authorization": f"Bearer {token}"}
response = session.get(f"{BASE_URL}/api/student/database?year=2025", headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    print("✅ Rota de database está funcionando!")
else:
    print(f"❌ Erro na rota: {response.text}")

# 3. Verificar o arquivo main.js
print("\n3️⃣  Verificando arquivo main.js...")
response = session.get(f"{BASE_URL}/static/js/main.d8c02d53.js", headers=headers)
print(f"Status: {response.status_code}")
print(f"Tamanho: {len(response.text)} bytes")

if 'monthly-database' in response.text:
    print("✅ 'monthly-database' encontrado no main.js")
else:
    print("❌ 'monthly-database' NÃO encontrado no main.js")

if 'to="catalog"' in response.text:
    print("⚠️  'to=\"catalog\"' encontrado (caminho relativo)")
else:
    print("✅ Sem 'to=\"catalog\"' (caminhos relativos)")

# 4. Verificar o index.html
print("\n4️⃣  Verificando index.html...")
response = session.get(f"{BASE_URL}/", headers=headers)
print(f"Status: {response.status_code}")

if 'main.d8c02d53.js' in response.text:
    print("✅ 'main.d8c02d53.js' encontrado no index.html (arquivo correto)")
else:
    print("❌ 'main.d8c02d53.js' NÃO encontrado no index.html")

print("\n✅ Teste concluído!")
print("\n📝 Próximos passos:")
print("1. Abra https://cardroomgrinders.com.br no navegador")
print("2. Faça login com: leandrokoles / leandrokoles123456")
print("3. Clique em 'Database Mensal' na sidebar")
print("4. Verifique se a URL é: https://cardroomgrinders.com.br/student/monthly-database")
print("5. Verifique se NÃO há repetição de '/catalog'")

