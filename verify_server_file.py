#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar primeiras 10 linhas do arquivo no servidor (poker-academy)\n')
stdin, stdout, stderr = client.exec_command('head -10 /root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar tamanho do arquivo no servidor (poker-academy)\n')
stdin, stdout, stderr = client.exec_command('wc -l /root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar primeiras 10 linhas do arquivo no servidor (poker-academy-backend)\n')
stdin, stdout, stderr = client.exec_command('head -10 /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar tamanho do arquivo no servidor (poker-academy-backend)\n')
stdin, stdout, stderr = client.exec_command('wc -l /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

client.close()

