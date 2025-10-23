#!/usr/bin/env python3
import requests
import io
import warnings

warnings.filterwarnings('ignore')

BASE_URL = 'https://cardroomgrinders.com.br'
USERNAME = 'leandrokoles'
PASSWORD = 'leandrokoles123456'

print('🧪 TESTE COMPLETO: UPLOAD + DOWNLOAD\n')

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
test_file = io.BytesIO(b'Test file content for April 2025')
test_file.name = 'test_april_2025.zip'
print(f'✅ Arquivo criado: {test_file.name}')

# 3. Upload
print('\n📝 Passo 3: Upload do arquivo\n')
files = {'file': test_file}
data = {'month': 'abr', 'year': 2025}
headers = {'Authorization': f'Bearer {token}'}
upload_response = requests.post(
    f'{BASE_URL}/api/student/database/upload',
    files=files,
    data=data,
    headers=headers,
    verify=False
)
print(f'Status: {upload_response.status_code}')
if upload_response.status_code == 200:
    result = upload_response.json()
    filename = result['data']['file_url'].split('/')[-1]
    print(f'✅ Upload bem-sucedido!')
    print(f'Filename: {filename}')
else:
    print(f'❌ Upload falhou: {upload_response.text}')
    exit(1)

# 4. Listar databases
print('\n📝 Passo 4: Listar databases\n')
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
for db in databases:
    print(f'  - {db["month"]}: {db["file_url"]}')

# 5. Download do arquivo enviado
print(f'\n📝 Passo 5: Download do arquivo enviado\n')
download_response = requests.get(
    f'{BASE_URL}/api/student/database/download/{filename}',
    headers=headers,
    verify=False
)
print(f'Status: {download_response.status_code}')
if download_response.status_code == 200:
    print(f'✅ Download bem-sucedido!')
    print(f'Tamanho: {len(download_response.content)} bytes')
else:
    print(f'❌ Download falhou: {download_response.text}')

print('\n✅ TESTE COMPLETO CONCLUÍDO COM SUCESSO!')

