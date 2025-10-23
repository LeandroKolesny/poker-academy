#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar estrutura de diretórios\n')
stdin, stdout, stderr = client.exec_command('ls -la /root/Dojo_Deploy/poker-academy/')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar se poker_academy_api existe\n')
stdin, stdout, stderr = client.exec_command('ls -la /root/Dojo_Deploy/poker-academy/poker_academy_api/ | head -20')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar arquivo database_routes.py\n')
stdin, stdout, stderr = client.exec_command('ls -la /root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar arquivo no backend\n')
stdin, stdout, stderr = client.exec_command('ls -la /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

client.close()

