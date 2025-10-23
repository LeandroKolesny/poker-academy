#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar linhas 160-185 do arquivo no servidor\n')
stdin, stdout, stderr = client.exec_command('sed -n "160,185p" /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar linhas 160-185 do arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend sed -n "160,185p" /app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

client.close()

