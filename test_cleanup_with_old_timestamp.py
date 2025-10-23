#!/usr/bin/env python3
import paramiko
import requests
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

BASE_URL = 'https://cardroomgrinders.com.br'
USERNAME = 'leandrokoles'
PASSWORD = 'leandrokoles123456'

print('🧪 TESTE: LAZY CLEANUP COM TIMESTAMP ANTIGO\n')

# 1. Login
print('📝 Passo 1: Login\n')
login_response = requests.post(
    f'{BASE_URL}/api/auth/login',
    json={'username': USERNAME, 'password': PASSWORD},
    verify=False
)
response_data = login_response.json()
if 'data' in response_data:
    token = response_data['data']['token']
else:
    token = response_data['token']
print(f'✅ Login bem-sucedido')

# 2. Conectar ao servidor e criar um arquivo antigo no banco
print('\n📝 Passo 2: Criar arquivo antigo no banco de dados\n')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

# Calcular timestamp de 6 minutos atrás
old_time = (datetime.now() - timedelta(minutes=6)).strftime('%Y-%m-%d %H:%M:%S')

sql_command = f"""
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
INSERT INTO student_database (student_id, month, year, file_url, file_size, created_at, updated_at)
VALUES (26, 'jun', 2025, '/api/uploads/databases/db_26_jun_2025_old.zip', 1000, '{old_time}', '{old_time}');
"
"""

stdin, stdout, stderr = client.exec_command(sql_command)
output = stdout.read().decode('utf-8')
print(f'✅ Arquivo antigo criado com timestamp: {old_time}')

# 3. Listar databases (arquivo antigo deve aparecer)
print('\n📝 Passo 3: Listar databases (arquivo antigo deve aparecer)\n')
headers = {'Authorization': f'Bearer {token}'}
list_response = requests.get(
    f'{BASE_URL}/api/student/database?year=2025',
    headers=headers,
    verify=False
)
response_data = list_response.json()
if isinstance(response_data, dict) and 'data' in response_data:
    databases = response_data['data']
    if isinstance(databases, dict) and 'data' in databases:
        databases = databases['data']
else:
    databases = response_data

print(f'✅ Databases encontrados: {len(databases)}')
jun_found = False
for db in databases:
    if db['month'] == 'jun':
        jun_found = True
        print(f'  ✅ Junho encontrado: {db["file_url"]}')

if not jun_found:
    print(f'  ❌ Junho NÃO encontrado!')

# 4. Listar databases novamente (arquivo antigo deve ter sido deletado)
print('\n📝 Passo 4: Listar databases novamente (arquivo antigo deve ter sido deletado)\n')
list_response = requests.get(
    f'{BASE_URL}/api/student/database?year=2025',
    headers=headers,
    verify=False
)
response_data = list_response.json()
if isinstance(response_data, dict) and 'data' in response_data:
    databases = response_data['data']
    if isinstance(databases, dict) and 'data' in databases:
        databases = databases['data']
else:
    databases = response_data

print(f'✅ Databases encontrados: {len(databases)}')
jun_found = False
for db in databases:
    if db['month'] == 'jun':
        jun_found = True
        print(f'  ❌ Junho ainda encontrado: {db["file_url"]}')

if not jun_found:
    print(f'  ✅ Junho foi deletado com sucesso!')

client.close()
print('\n✅ TESTE CONCLUÍDO!')

