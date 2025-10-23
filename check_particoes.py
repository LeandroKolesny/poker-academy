#!/usr/bin/env python3
import requests
import warnings

warnings.filterwarnings('ignore')

BASE_URL = 'https://cardroomgrinders.com.br'
USERNAME = 'leandrokoles'
PASSWORD = 'leandrokoles123456'

print('🔍 VERIFICAR PARTIÇÕES NO SISTEMA\n')

# Login
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

headers = {'Authorization': f'Bearer {token}'}

# Buscar partições
print('📝 Buscando partições...\n')
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
    
    print(f'✅ {len(particoes)} partição(ões) encontrada(s):\n')
    for p in particoes:
        print(f'   ID: {p["id"]}')
        print(f'   Nome: {p["nome"]}')
        print(f'   Descrição: {p["descricao"]}')
        print()
else:
    print(f'❌ Erro: {particoes_response.status_code}')
    print(particoes_response.text)

