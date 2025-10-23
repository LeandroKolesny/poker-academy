#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

# Criar script no servidor
script_content = '''import requests
import json

# Login
login_response = requests.post(
    "http://localhost:5000/api/auth/login",
    json={"username": "leandrokoles", "password": "leandrokoles123456"}
)
print(f"Login status: {login_response.status_code}")
login_data = login_response.json()
token = login_data["data"]["token"]
print(f"Token: {token[:50]}...")

# GET databases
headers = {"Authorization": f"Bearer {token}"}
db_response = requests.get(
    "http://localhost:5000/api/student/database?year=2025",
    headers=headers
)
print(f"\\nGET /api/student/database status: {db_response.status_code}")
print(f"Response: {json.dumps(db_response.json(), indent=2)}")
'''

print('📝 Criando script no servidor...\n')
stdin, stdout, stderr = client.exec_command('cat > /tmp/test_api.py << \'EOF\'\n' + script_content + '\nEOF')
stdout.read()

print('📝 Executando script...\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend python /tmp/test_api.py')
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(output)
if error:
    print(f"Erro: {error}")

client.close()

