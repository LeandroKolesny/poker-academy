#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Teste 1: Fazer login\n')
stdin, stdout, stderr = client.exec_command('''curl -s -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d '{"username":"leandrokoles","password":"leandrokoles123456"}'  2>&1''')
login_response = stdout.read().decode('utf-8')
print(login_response[:500])

# Extrair token
import json
try:
    login_data = json.loads(login_response)
    token = login_data['data']['token']
    print(f'\n✅ Token obtido: {token[:50]}...')
except:
    print('\n❌ Erro ao extrair token')
    token = None

if token:
    print('\n\n📝 Teste 2: GET /api/student/database?year=2025\n')
    stdin, stdout, stderr = client.exec_command(f'curl -s -X GET "http://localhost:5000/api/student/database?year=2025" -H "Authorization: Bearer {token}" 2>&1')
    response = stdout.read().decode('utf-8')
    print(response[:1000])

client.close()

