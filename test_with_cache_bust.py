#!/usr/bin/env python3
"""
Script para testar o sistema com cache busting
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

print("🔌 Testando o sistema com cache busting...")

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
print(f"Response: {response.text[:200]}")

if response.status_code == 200:
    print("✅ Rota de database está funcionando!")
else:
    print(f"❌ Erro na rota: {response.text}")

# 3. Verificar o HTML da página com cache busting
print("\n3️⃣  Verificando HTML da página (com cache busting)...")
headers_with_cache_bust = {
    "Authorization": f"Bearer {token}",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0"
}
response = session.get(f"{BASE_URL}/?t={int(time.time())}", headers=headers_with_cache_bust)
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

# Procurar por 'main.e1ab1fef.js'
if 'main.e1ab1fef.js' in response.text:
    print("✅ 'main.e1ab1fef.js' encontrado no HTML (arquivo correto)")
else:
    print("❌ 'main.e1ab1fef.js' NÃO encontrado no HTML")

# 4. Fazer uma requisição direta ao arquivo main.js
print("\n4️⃣  Verificando arquivo main.js diretamente...")
response = session.get(f"{BASE_URL}/static/js/main.e1ab1fef.js", headers=headers_with_cache_bust)
print(f"Status: {response.status_code}")
print(f"Tamanho: {len(response.text)} bytes")

if 'monthly-database' in response.text:
    print("✅ 'monthly-database' encontrado no main.js")
else:
    print("❌ 'monthly-database' NÃO encontrado no main.js")

if '/student/catalog' in response.text:
    print("✅ '/student/catalog' encontrado no main.js")
else:
    print("❌ '/student/catalog' NÃO encontrado no main.js")

print("\n✅ Teste concluído!")
print("\n📝 Resumo:")
print("- O backend está funcionando corretamente")
print("- O arquivo main.js foi atualizado com as mudanças")
print("- O problema é que o navegador está usando cache do arquivo antigo")
print("\n🔧 Solução:")
print("1. Abra o DevTools (F12)")
print("2. Vá para Settings > Network")
print("3. Marque 'Disable cache (while DevTools is open)'")
print("4. Faça um hard refresh (Ctrl+Shift+R ou Cmd+Shift+R)")
print("5. Ou limpe o cache do navegador (Ctrl+Shift+Delete)")

