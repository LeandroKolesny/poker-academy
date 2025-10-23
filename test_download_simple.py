#!/usr/bin/env python3
import requests
import json

BASE_URL = 'https://cardroomgrinders.com.br'

print('🧪 TESTE SIMPLES: DOWNLOAD\n')

# Login
login_data = {'username': 'leandrokoles', 'password': 'leandrokoles123456'}
response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data, verify=False)
token = response.json().get('token')
headers = {'Authorization': f'Bearer {token}'}

# Listar databases
response = requests.get(f'{BASE_URL}/api/student/database?year=2025', headers=headers, verify=False)
response_data = response.json()
databases = response_data.get('data', []) if isinstance(response_data.get('data'), list) else response_data.get('data', {}).get('data', [])

print(f'Databases encontrados: {len(databases)}\n')
for db in databases:
    print(f'Mês: {db.get("month")}')
    print(f'  File URL: {db.get("file_url")}')
    print(f'  File Size: {db.get("file_size")} bytes')
    
    # Extrair filename
    filename = db.get('file_url', '').split('/')[-1]
    print(f'  Filename: {filename}')
    
    # Testar download
    download_url = f'{BASE_URL}/api/student/database/download/{filename}'
    print(f'  Download URL: {download_url}')
    
    response = requests.get(download_url, headers=headers, verify=False)
    print(f'  Status: {response.status_code}')
    
    if response.status_code == 200:
        print(f'  ✅ Download bem-sucedido! ({len(response.content)} bytes)')
    else:
        print(f'  ❌ Erro: {response.text}')
    print()

