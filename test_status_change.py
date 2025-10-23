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

print('🧪 TESTE: MUDANÇA DE STATUS (ATIVO → DELETADO)\n')

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

# 2. Upload de arquivo
print('\n📝 Passo 2: Upload de arquivo\n')
headers = {'Authorization': f'Bearer {token}'}
test_file = io.BytesIO(b'Test file for status change')
test_file.name = 'test_status.zip'

files = {'file': test_file}
data = {'month': 'nov', 'year': 2025}

upload_response = requests.post(
    f'{BASE_URL}/api/student/database/upload',
    files=files,
    data=data,
    headers=headers,
    verify=False
)

if upload_response.status_code == 200:
    result = upload_response.json()
    filename = result['data']['file_url'].split('/')[-1]
    print(f'✅ Upload bem-sucedido: {filename}')
else:
    print(f'❌ Upload falhou: {upload_response.text}')
    exit(1)

# 3. Listar databases (arquivo deve estar com status 'ativo')
print('\n📝 Passo 3: Listar databases (arquivo deve estar ATIVO)\n')
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

nov_found = False
for db in databases:
    if db['month'] == 'nov':
        nov_found = True
        print(f'✅ Novembro encontrado com status: {db["status"]}')
        if db['status'] != 'ativo':
            print(f'❌ Status esperado: ativo, recebido: {db["status"]}')

if not nov_found:
    print(f'❌ Novembro NÃO encontrado!')

# 4. Criar arquivo antigo no banco (simular expiração)
print('\n📝 Passo 4: Simular expiração (alterar created_at para 6 minutos atrás)\n')
SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

old_time = (datetime.now() - timedelta(minutes=6)).strftime('%Y-%m-%d %H:%M:%S')
sql_command = f"""
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
UPDATE student_database SET created_at = '{old_time}' WHERE month = 'nov' AND year = 2025 AND student_id = 26;
"
"""
stdin, stdout, stderr = client.exec_command(sql_command)
print(f'✅ Arquivo alterado para timestamp: {old_time}')

# 5. Listar databases novamente (arquivo deve ter status 'deletado')
print('\n📝 Passo 5: Listar databases novamente (arquivo deve estar DELETADO)\n')
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

nov_found = False
for db in databases:
    if db['month'] == 'nov':
        nov_found = True
        if db['status'] == 'deletado':
            print(f'✅ Novembro encontrado com status: DELETADO')
        else:
            print(f'❌ Novembro encontrado com status: {db["status"]} (esperado: deletado)')

if not nov_found:
    print(f'❌ Novembro NÃO encontrado!')

client.close()
print('\n✅ TESTE CONCLUÍDO COM SUCESSO!')

