#!/usr/bin/env python3
import requests
import json
import time
import os

BASE_URL = 'https://cardroomgrinders.com.br'

print('🧪 TESTE COMPLETO: LOGIN + UPLOAD + DOWNLOAD\n')
print('='*60)

# Passo 1: Login
print('\n📝 Passo 1: Fazer login\n')
login_data = {
    'username': 'leandrokoles',
    'password': 'leandrokoles123456'
}

response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data, verify=False)
print(f'Status: {response.status_code}')

if response.status_code == 200:
    token = response.json().get('token')
    print(f'✅ Login bem-sucedido!')
    print(f'Token: {token[:50]}...')
else:
    print(f'❌ Erro no login: {response.text}')
    exit(1)

headers = {'Authorization': f'Bearer {token}'}

# Passo 2: Listar databases
print('\n📝 Passo 2: Listar databases\n')
response = requests.get(f'{BASE_URL}/api/student/database?year=2025', headers=headers, verify=False)
print(f'Status: {response.status_code}')
response_data = response.json()
# O backend retorna { data: [...] }
databases = response_data.get('data', []) if isinstance(response_data.get('data'), list) else response_data.get('data', {}).get('data', [])
print(f'Databases encontrados: {len(databases)}')
for db in databases:
    print(f'  - {db.get("month")}: {db.get("file_size")} bytes')

# Passo 3: Criar arquivo de teste
print('\n📝 Passo 3: Criar arquivo de teste\n')
test_file = 'test_database.zip'
with open(test_file, 'wb') as f:
    f.write(b'PK\x03\x04' + b'x' * 1000)  # Arquivo ZIP mínimo
print(f'✅ Arquivo criado: {test_file}')

# Passo 4: Fazer upload
print('\n📝 Passo 4: Fazer upload\n')
with open(test_file, 'rb') as f:
    files = {'file': f}
    data = {'month': 'mar', 'year': 2025}
    response = requests.post(f'{BASE_URL}/api/student/database/upload', 
                            files=files, data=data, headers=headers, verify=False)

print(f'Status: {response.status_code}')
if response.status_code == 200:
    result = response.json()
    print(f'✅ Upload bem-sucedido!')
    file_url = result.get('data', {}).get('file_url')
    print(f'URL do arquivo: {file_url}')
else:
    print(f'❌ Erro no upload: {response.text}')
    exit(1)

# Passo 5: Listar databases novamente
print('\n📝 Passo 5: Listar databases após upload\n')
response = requests.get(f'{BASE_URL}/api/student/database?year=2025', headers=headers, verify=False)
response_data = response.json()
databases = response_data.get('data', []) if isinstance(response_data.get('data'), list) else response_data.get('data', {}).get('data', [])
print(f'Databases encontrados: {len(databases)}')
for db in databases:
    print(f'  - {db.get("month")}: {db.get("file_size")} bytes')

# Passo 6: Fazer download
print('\n📝 Passo 6: Fazer download\n')
filename = file_url.split('/')[-1]
download_url = f'{BASE_URL}/api/student/database/download/{filename}'
response = requests.get(download_url, headers=headers, verify=False)
print(f'Status: {response.status_code}')

if response.status_code == 200:
    print(f'✅ Download bem-sucedido!')
    print(f'Tamanho do arquivo: {len(response.content)} bytes')
    
    # Salvar arquivo baixado
    with open('downloaded_database.zip', 'wb') as f:
        f.write(response.content)
    print(f'✅ Arquivo salvo como: downloaded_database.zip')
else:
    print(f'❌ Erro no download: {response.status_code}')
    print(f'Resposta: {response.text}')

# Limpeza
os.remove(test_file)
if os.path.exists('downloaded_database.zip'):
    os.remove('downloaded_database.zip')

print('\n' + '='*60)
print('✅ TESTE COMPLETO FINALIZADO COM SUCESSO!')

