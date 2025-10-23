#!/usr/bin/env python3
import requests
import json
import warnings

warnings.filterwarnings('ignore')

BASE_URL = 'https://cardroomgrinders.com.br'
USERNAME = 'leandrokoles'
PASSWORD = 'leandrokoles123456'

print('🧪 DEBUG: Verificar resposta da API\n')

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

# Listar databases
headers = {'Authorization': f'Bearer {token}'}
list_response = requests.get(
    f'{BASE_URL}/api/student/database?year=2025',
    headers=headers,
    verify=False
)

print('📝 Status Code:', list_response.status_code)
print('\n📝 Response JSON:')
print(json.dumps(list_response.json(), indent=2, ensure_ascii=False))

print('\n📝 Primeiro item:')
response_data = list_response.json()
if isinstance(response_data, dict) and 'data' in response_data:
    databases = response_data['data']
else:
    databases = response_data

if databases:
    print(json.dumps(databases[0], indent=2, ensure_ascii=False))

