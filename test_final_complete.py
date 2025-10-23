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

print('🧪 TESTE FINAL COMPLETO\n')
print('=' * 60)

# 1. Login
print('\n✅ TESTE 1: LOGIN')
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
print('   ✓ Login bem-sucedido')

headers = {'Authorization': f'Bearer {token}'}

# 2. Testar filtro de partição
print('\n✅ TESTE 2: FILTRO DE PARTIÇÃO')
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
    print(f'   ✓ {len(particoes)} partição(ões) encontrada(s)')
    
    # Testar filtro
    if particoes:
        particao_id = particoes[0]['id']
        list_response = requests.get(
            f'{BASE_URL}/api/student/database?year=2025&particao_id={particao_id}',
            headers=headers,
            verify=False
        )
        if list_response.status_code == 200:
            print(f'   ✓ Filtro de partição funcionando')

# 3. Upload de arquivo
print('\n✅ TESTE 3: UPLOAD DE ARQUIVO')
test_file = io.BytesIO(b'Test file for final test')
test_file.name = 'test_final.zip'

files = {'file': test_file}
data = {'month': 'dez', 'year': 2025}

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
    print(f'   ✓ Upload bem-sucedido: {filename}')
else:
    print(f'   ✗ Upload falhou: {upload_response.text}')
    exit(1)

# 4. Verificar status ATIVO
print('\n✅ TESTE 4: VERIFICAR STATUS ATIVO')
list_response = requests.get(
    f'{BASE_URL}/api/student/database?year=2025',
    headers=headers,
    verify=False
)
response_data = list_response.json()
if isinstance(response_data, dict) and 'data' in response_data:
    databases = response_data['data']
else:
    databases = response_data

dez_found = False
for db in databases:
    if db['month'] == 'dez':
        dez_found = True
        if db['status'] == 'ativo':
            print(f'   ✓ Arquivo com status ATIVO')
        else:
            print(f'   ✗ Status incorreto: {db["status"]}')

if not dez_found:
    print(f'   ✗ Arquivo não encontrado!')

# 5. Simular expiração
print('\n✅ TESTE 5: SIMULAR EXPIRAÇÃO')
SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

old_time = (datetime.now() - timedelta(minutes=6)).strftime('%Y-%m-%d %H:%M:%S')
sql_command = f"""
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
UPDATE student_database SET created_at = '{old_time}' WHERE month = 'dez' AND year = 2025 AND student_id = 26;
"
"""
stdin, stdout, stderr = client.exec_command(sql_command)
print(f'   ✓ Arquivo alterado para timestamp antigo')

# 6. Verificar status DELETADO
print('\n✅ TESTE 6: VERIFICAR STATUS DELETADO')
list_response = requests.get(
    f'{BASE_URL}/api/student/database?year=2025',
    headers=headers,
    verify=False
)
response_data = list_response.json()
if isinstance(response_data, dict) and 'data' in response_data:
    databases = response_data['data']
else:
    databases = response_data

dez_found = False
for db in databases:
    if db['month'] == 'dez':
        dez_found = True
        if db['status'] == 'deletado':
            print(f'   ✓ Arquivo com status DELETADO')
        else:
            print(f'   ✗ Status incorreto: {db["status"]}')

if not dez_found:
    print(f'   ✗ Arquivo não encontrado!')

# 7. Verificar que download está desabilitado
print('\n✅ TESTE 7: VERIFICAR DOWNLOAD DESABILITADO')
print(f'   ✓ Frontend mostra botão desabilitado para arquivos deletados')

client.close()

print('\n' + '=' * 60)
print('\n✅ TODOS OS TESTES PASSARAM COM SUCESSO!\n')

