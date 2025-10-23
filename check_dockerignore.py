#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar .dockerignore\n')
stdin, stdout, stderr = client.exec_command('cat /root/Dojo_Deploy/poker-academy/.dockerignore 2>/dev/null || echo "Arquivo não existe"')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar arquivo no servidor\n')
stdin, stdout, stderr = client.exec_command('ls -la /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -la /app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

client.close()

