#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('⏳ Aguardando 10 segundos para backend estabilizar...')
time.sleep(10)

print('\n📝 Teste 1: Verificando se o backend está respondendo\n')
stdin, stdout, stderr = client.exec_command('curl -s http://localhost:5000/api/health')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 2: Verificando logs do backend\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -30')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 3: Verificando se o arquivo ainda está no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lah /app/uploads/databases/')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 4: Testando endpoint de download (sem autenticação)\n')
stdin, stdout, stderr = client.exec_command('curl -s -I http://localhost:5000/api/uploads/databases/db_26_jan_2025_09ad111a.zip')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 5: Testando GET /api/student/database\n')
stdin, stdout, stderr = client.exec_command('curl -s -H "Authorization: Bearer test" http://localhost:5000/api/student/database?year=2025 | head -20')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Testes concluídos!')

