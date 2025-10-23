#!/usr/bin/env python3
import paramiko
import json

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Teste 1: Fazer login e obter token\n')
stdin, stdout, stderr = client.exec_command('''curl -s -X POST http://localhost:5000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"username":"leandrokoles","password":"leandrokoles123456"}' | python -c "import sys, json; data = json.load(sys.stdin); print(data.get('data', {}).get('token', 'ERRO'))"''')
token = stdout.read().decode('utf-8').strip()
print(f'Token: {token[:50]}...\n')

print('📝 Teste 2: Fazer GET /api/student/database?year=2025\n')
stdin, stdout, stderr = client.exec_command(f'''curl -s -X GET "http://localhost:5000/api/student/database?year=2025" \\
  -H "Authorization: Bearer {token}" \\
  -H "Content-Type: application/json"''')
response = stdout.read().decode('utf-8')
print(response)

print('\n\n📝 Teste 3: Verificar logs do backend para essa requisição\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | grep "student/database" | tail -5')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 4: Verificar banco de dados - todos os registros\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, student_id, month, year, file_url, file_size, created_at FROM student_database ORDER BY id DESC;"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

client.close()

