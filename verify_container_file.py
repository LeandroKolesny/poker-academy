#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend cat /app/src/routes/database_routes.py | head -15')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Procurar send_file no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep -n "send_file" /app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Procurar send_from_directory no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep -n "send_from_directory" /app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

client.close()

