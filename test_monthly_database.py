#!/usr/bin/env python3
"""
Script para testar a funcionalidade de Database Mensal
"""
import requests
import json
import io
import zipfile
from datetime import datetime

# Configurações
API_URL = "https://cardroomgrinders.com.br/api"
STUDENT_USERNAME = "leandrokoles"
STUDENT_PASSWORD = "123456"

print("=" * 60)
print("🧪 TESTE DE DATABASE MENSAL")
print("=" * 60)

# 1. Login como aluno
print("\n1️⃣  Fazendo login como aluno...")
login_response = requests.post(
    f"{API_URL}/auth/login",
    json={"username": STUDENT_USERNAME, "password": STUDENT_PASSWORD},
    verify=False
)

if login_response.status_code != 200:
    print(f"❌ Erro no login: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()['data']['token']
print(f"✅ Login bem-sucedido! Token: {token[:20]}...")

headers = {"Authorization": f"Bearer {token}"}

# 2. Criar arquivo .zip de teste
print("\n2️⃣  Criando arquivo .zip de teste...")
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    # Adicionar alguns arquivos de teste
    zip_file.writestr('hand_1.txt', 'Hand 1 data')
    zip_file.writestr('hand_2.txt', 'Hand 2 data')
    zip_file.writestr('hand_3.txt', 'Hand 3 data')

zip_buffer.seek(0)
print(f"✅ Arquivo .zip criado! Tamanho: {len(zip_buffer.getvalue())} bytes")

# 3. Fazer upload do arquivo
print("\n3️⃣  Fazendo upload do arquivo...")
files = {'file': ('test_database.zip', zip_buffer, 'application/zip')}
data = {'month': 'jan', 'year': 2025}

upload_response = requests.post(
    f"{API_URL}/student/database/upload",
    files=files,
    data=data,
    headers=headers,
    verify=False
)

print(f"Status: {upload_response.status_code}")
if upload_response.status_code != 200:
    print(f"❌ Erro no upload: {upload_response.text}")
else:
    print(f"✅ Upload bem-sucedido!")
    print(f"Response: {upload_response.json()}")

# 4. Listar databases do aluno
print("\n4️⃣  Listando databases do aluno...")
list_response = requests.get(
    f"{API_URL}/student/database?year=2025",
    headers=headers,
    verify=False
)

if list_response.status_code != 200:
    print(f"❌ Erro ao listar: {list_response.status_code}")
    print(list_response.text)
else:
    databases = list_response.json()['data']
    print(f"✅ Databases encontrados: {len(databases)}")
    for db in databases:
        print(f"   - Mês: {db['month']}, Tamanho: {db['file_size']} bytes")

# 5. Fazer download do arquivo
print("\n5️⃣  Fazendo download do arquivo...")
if databases:
    filename = databases[0]['file_url'].split('/')[-1]
    download_response = requests.get(
        f"{API_URL}/student/database/download/{filename}",
        headers=headers,
        verify=False
    )
    
    if download_response.status_code != 200:
        print(f"❌ Erro no download: {download_response.status_code}")
    else:
        print(f"✅ Download bem-sucedido!")
        print(f"   Tamanho do arquivo: {len(download_response.content)} bytes")
        
        # Verificar se é um arquivo .zip válido
        try:
            with zipfile.ZipFile(io.BytesIO(download_response.content)) as z:
                print(f"   Arquivos no .zip: {z.namelist()}")
        except:
            print("   ⚠️  Arquivo não é um .zip válido")

# 6. Testar validação de arquivo
print("\n6️⃣  Testando validação de arquivo (deve falhar)...")
invalid_file = io.BytesIO(b"This is not a zip file")
files = {'file': ('invalid.txt', invalid_file, 'text/plain')}
data = {'month': 'fev', 'year': 2025}

invalid_response = requests.post(
    f"{API_URL}/student/database/upload",
    files=files,
    data=data,
    headers=headers,
    verify=False
)

if invalid_response.status_code != 200:
    print(f"✅ Validação funcionou! Status: {invalid_response.status_code}")
    print(f"   Erro: {invalid_response.json()['error']}")
else:
    print(f"❌ Validação não funcionou!")

print("\n" + "=" * 60)
print("✅ TESTES CONCLUÍDOS!")
print("=" * 60)

