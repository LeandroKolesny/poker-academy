#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar arquivo em poker-academy-backend\n')
stdin, stdout, stderr = client.exec_command('grep "send_file" /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py | head -1')
output = stdout.read().decode('utf-8')
print(f"send_file: {output}")

print('\n📝 Verificar arquivo em poker-academy\n')
stdin, stdout, stderr = client.exec_command('grep "send_file" /root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py | head -1')
output = stdout.read().decode('utf-8')
print(f"send_file: {output}")

print('\n📝 Verificar arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep "send_file" /app/src/routes/database_routes.py | head -1')
output = stdout.read().decode('utf-8')
print(f"send_file: {output}")

client.close()

