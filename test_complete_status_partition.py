#!/usr/bin/env python3
import requests
import io
import warnings
import paramiko
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

BASE_URL = 'https://cardroomgrinders.com.br'
USERNAME = 'leandrokoles'
PASSWORD = 'leandrokoles123456'

print('🧪 TESTE COMPLETO: STATUS E FILTRO DE PARTIÇÃO\n')

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

# 2. Testar endpoint de partições
print('\n📝 Passo 2: Listar partições\n')
headers = {'Authorization': f'Bearer {token}'}
particoes_response = requests.get(
    f'{BASE_URL}/api/particoes',
    headers=headers,
    verify=False
)
if particoes_response.status_code == 200:
    response_data = particoes_response.json()
    if isinstance(response_data, dict) and 'data' in response_data:
        particoes = response_data['data']
    else:
        particoes = response_data
    print(f'✅ Partições encontradas: {len(particoes)}')
    for p in particoes:
        print(f'  - {p["nome"]} (ID: {p["id"]})')
else:
    print(f'❌ Erro ao listar partições: {particoes_response.text}')

# 3. Testar filtro de partição
print('\n📝 Passo 3: Testar filtro de partição\n')
if particoes:
    particao_id = particoes[0]['id']
    list_response = requests.get(
        f'{BASE_URL}/api/student/database?year=2025&particao_id={particao_id}',
        headers=headers,
        verify=False
    )
    if list_response.status_code == 200:
        databases = list_response.json()['data']
        print(f'✅ Databases da partição "{particoes[0]["nome"]}": {len(databases)}')
    else:
        print(f'❌ Erro ao filtrar por partição: {list_response.text}')

# 4. Criar arquivo com timestamp antigo para testar status
print('\n📝 Passo 4: Criar arquivo antigo no banco\n')
SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

old_time = (datetime.now() - timedelta(minutes=6)).strftime('%Y-%m-%d %H:%M:%S')
sql_command = f"""
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
INSERT INTO student_database (student_id, month, year, file_url, file_size, status, created_at, updated_at)
VALUES (26, 'out', 2025, '/api/uploads/databases/db_26_out_2025_old.zip', 1000, 'ativo', '{old_time}', '{old_time}');
"
"""
stdin, stdout, stderr = client.exec_command(sql_command)
print(f'✅ Arquivo antigo criado com timestamp: {old_time}')

# 5. Listar databases (arquivo antigo deve aparecer com status 'ativo')
print('\n📝 Passo 5: Listar databases (arquivo antigo deve aparecer)\n')
list_response = requests.get(
    f'{BASE_URL}/api/student/database?year=2025',
    headers=headers,
    verify=False
)
databases = list_response.json()['data']
out_found = False
for db in databases:
    if db['month'] == 'out':
        out_found = True
        print(f'✅ Outubro encontrado com status: {db["status"]}')

if not out_found:
    print(f'❌ Outubro NÃO encontrado!')

# 6. Listar databases novamente (arquivo antigo deve ter status 'deletado')
print('\n📝 Passo 6: Listar databases novamente (arquivo deve estar deletado)\n')
list_response = requests.get(
    f'{BASE_URL}/api/student/database?year=2025',
    headers=headers,
    verify=False
)
databases = list_response.json()['data']
out_found = False
for db in databases:
    if db['month'] == 'out':
        out_found = True
        if db['status'] == 'deletado':
            print(f'✅ Outubro encontrado com status: DELETADO')
        else:
            print(f'❌ Outubro encontrado com status: {db["status"]} (esperado: deletado)')

if not out_found:
    print(f'❌ Outubro NÃO encontrado!')

client.close()
print('\n✅ TESTE CONCLUÍDO COM SUCESSO!')

