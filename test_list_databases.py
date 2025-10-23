#!/usr/bin/env python3
import paramiko
import json

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Teste 1: Verificando banco de dados\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, student_id, month, year, file_url, file_size FROM student_database;"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

print('\n\n📝 Teste 2: Testando GET /api/student/database com curl\n')
stdin, stdout, stderr = client.exec_command('curl -s -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNiwidXNlcl90eXBlIjoic3R1ZGVudCIsImV4cCI6MTc2MDc1NDc0MX0.test" http://localhost:5000/api/student/database?year=2025 | python -m json.tool 2>/dev/null || echo "Erro ao parsear JSON"')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 3: Verificando logs do backend para requisições\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | grep "student/database" | tail -10')
output = stdout.read().decode('utf-8')
print(output)

client.close()

