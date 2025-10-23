#!/usr/bin/env python3
import paramiko
import time
import os

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Teste 1: Criar arquivo .zip de teste\n')
stdin, stdout, stderr = client.exec_command('cd /tmp && echo "test data" > test.txt && zip test.zip test.txt && ls -lh test.zip')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 2: Fazer login e obter token\n')
stdin, stdout, stderr = client.exec_command('curl -s -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d \'{"username":"leandrokoles","password":"leandrokoles123456"}\' | python -m json.tool 2>/dev/null | head -20')
output = stdout.read().decode('utf-8')
print(output)

# Extrair token
stdin, stdout, stderr = client.exec_command('curl -s -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d \'{"username":"leandrokoles","password":"leandrokoles123456"}\' | python -c "import sys, json; print(json.load(sys.stdin)[\'data\'][\'token\'])" 2>/dev/null')
token = stdout.read().decode('utf-8').strip()
print(f'\n✅ Token obtido: {token[:50]}...')

print('\n\n📝 Teste 3: Fazer upload do arquivo\n')
stdin, stdout, stderr = client.exec_command(f'curl -s -X POST http://localhost:5000/api/student/database/upload -H "Authorization: Bearer {token}" -F "file=@/tmp/test.zip" -F "month=fev" -F "year=2025" | python -m json.tool 2>/dev/null')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 4: Verificar se o arquivo foi salvo\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lah /app/uploads/databases/ | grep -v "^total"')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 5: Verificar banco de dados\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, student_id, month, year, file_size FROM student_database ORDER BY id DESC LIMIT 3;"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

client.close()
print('\n✅ Testes concluídos!')

