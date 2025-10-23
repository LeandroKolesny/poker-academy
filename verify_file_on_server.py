#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar arquivo no servidor\n')
stdin, stdout, stderr = client.exec_command('grep -n "send_from_directory" /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(f"Ocorrências de 'send_from_directory':\n{output}")

print('\n📝 Verificar se send_file está importado\n')
stdin, stdout, stderr = client.exec_command('head -15 /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar arquivo dentro do container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep -n "send_from_directory" /app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(f"Ocorrências no container:\n{output}")

client.close()

