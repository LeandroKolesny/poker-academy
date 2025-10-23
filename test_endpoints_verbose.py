#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Teste 1: Health check com verbose\n')
stdin, stdout, stderr = client.exec_command('curl -v http://localhost:5000/api/health 2>&1 | head -30')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 2: Testando endpoint /api/uploads/databases/\n')
stdin, stdout, stderr = client.exec_command('curl -v http://localhost:5000/api/uploads/databases/db_26_jan_2025_09ad111a.zip 2>&1 | head -50')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 3: Verificando rotas registradas no Flask\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend python -c "from src.main import app; print([str(rule) for rule in app.url_map.iter_rules() if \"database\" in str(rule)])" 2>&1')
output = stdout.read().decode('utf-8')
print(output)

client.close()

