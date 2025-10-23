#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Passo 1: Copiar arquivo via SFTP\n')
sftp = client.open_sftp()
local_file = 'poker-academy-backend/poker_academy_api/src/routes/database_routes.py'
remote_file = '/root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py'
sftp.put(local_file, remote_file)
print(f'✅ Arquivo copiado: {local_file} -> {remote_file}')
sftp.close()

print('\n📝 Passo 2: Verificar arquivo no servidor\n')
stdin, stdout, stderr = client.exec_command('head -5 /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 3: Parar backend\n')
stdin, stdout, stderr = client.exec_command('docker stop poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 4: Remover container e imagem\n')
stdin, stdout, stderr = client.exec_command('docker rm poker_backend && docker rmi poker-academy_backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 5: Rebuild\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d backend')
output = stdout.read().decode('utf-8')
print(output[-500:])

print('\n📝 Passo 6: Aguardar 15 segundos\n')
time.sleep(15)

print('📝 Passo 7: Verificar arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend head -5 /app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Deploy concluído!')

