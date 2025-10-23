#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Teste 1: Acessando via NGINX (localhost)\n')
stdin, stdout, stderr = client.exec_command('curl -s -I http://localhost/api/uploads/databases/db_26_jan_2025_09ad111a.zip')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 2: Acessando via NGINX com domínio\n')
stdin, stdout, stderr = client.exec_command('curl -s -I -H "Host: cardroomgrinders.com.br" http://localhost/api/uploads/databases/db_26_jan_2025_09ad111a.zip')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Teste 3: Verificando logs do NGINX\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_frontend 2>&1 | tail -30')
output = stdout.read().decode('utf-8')
print(output)

client.close()

