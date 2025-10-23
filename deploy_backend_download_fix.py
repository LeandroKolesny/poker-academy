#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Passo 1: Copiar arquivo corrigido para o servidor\n')
sftp = client.open_sftp()
sftp.put('poker-academy-backend/poker_academy_api/src/routes/database_routes.py',
         '/root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
print('✅ database_routes.py copiado')
sftp.close()

print('\n📝 Passo 2: Rebuildar backend\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 3: Aguardar rebuild (20 segundos)\n')
time.sleep(20)

print('📝 Passo 4: Verificar status\n')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 5: Verificar logs do backend\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -15')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Backend atualizado!')

