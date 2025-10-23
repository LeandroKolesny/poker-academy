#!/usr/bin/env python3
import requests
import io
import time
import warnings

warnings.filterwarnings('ignore')

BASE_URL = 'https://cardroomgrinders.com.br'
USERNAME = 'leandrokoles'
PASSWORD = 'leandrokoles123456'

print('🧪 TESTE: LAZY CLEANUP (5 MINUTOS)\n')

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

# 2. Criar arquivo de teste
print('\n📝 Passo 2: Criar arquivo de teste\n')
test_file = io.BytesIO(b'Test file for cleanup')
test_file.name = 'test_cleanup.zip'
print(f'✅ Arquivo criado: {test_file.name}')

# 3. Upload
print('\n📝 Passo 3: Upload do arquivo\n')
files = {'file': test_file}
data = {'month': 'mai', 'year': 2025}
headers = {'Authorization': f'Bearer {token}'}
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
    print(f'✅ Upload bem-sucedido!')
    print(f'Filename: {filename}')
else:
    print(f'❌ Upload falhou: {upload_response.text}')
    exit(1)

# 4. Listar databases (arquivo deve aparecer)
print('\n📝 Passo 4: Listar databases (arquivo deve aparecer)\n')
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
mai_found = False
for db in databases:
    if db['month'] == 'mai':
        mai_found = True
        print(f'  ✅ Maio encontrado: {db["file_url"]}')

if not mai_found:
    print(f'  ❌ Maio NÃO encontrado!')

# 5. Aguardar 5 minutos
print('\n📝 Passo 5: Aguardando 5 minutos (para teste, vamos aguardar 10 segundos)\n')
print('⏳ Aguardando 10 segundos...')
time.sleep(10)

# 6. Listar databases novamente (arquivo deve ter sido deletado)
print('\n📝 Passo 6: Listar databases novamente (arquivo deve ter sido deletado)\n')
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
mai_found = False
for db in databases:
    if db['month'] == 'mai':
        mai_found = True
        print(f'  ❌ Maio ainda encontrado: {db["file_url"]}')

if not mai_found:
    print(f'  ✅ Maio foi deletado com sucesso!')

print('\n✅ TESTE CONCLUÍDO!')

