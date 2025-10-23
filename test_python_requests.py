#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Teste: Executar Python script no servidor\n')

script = '''
import requests
import json

# Login
login_response = requests.post(
    'http://localhost:5000/api/auth/login',
    json={'username': 'leandrokoles', 'password': 'leandrokoles123456'}
)
print(f"Login status: {login_response.status_code}")
login_data = login_response.json()
token = login_data['data']['token']
print(f"Token: {token[:50]}...")

# GET databases
headers = {'Authorization': f'Bearer {token}'}
db_response = requests.get(
    'http://localhost:5000/api/student/database?year=2025',
    headers=headers
)
print(f"\\nGET /api/student/database status: {db_response.status_code}")
print(f"Response: {json.dumps(db_response.json(), indent=2)}")
'''

stdin, stdout, stderr = client.exec_command(f'docker exec poker_backend python -c "{script}"')
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(output)
if error:
    print(f"Erro: {error}")

client.close()

