#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🔨 FORÇAR REBUILD DO BACKEND\n')

print('📝 Passo 1: Remover container antigo\n')
stdin, stdout, stderr = client.exec_command('docker rm -f poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 2: Remover imagem antiga\n')
stdin, stdout, stderr = client.exec_command('docker rmi poker-academy_backend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 3: Rebuildar backend\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build backend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 4: Aguardar 20 segundos\n')
time.sleep(20)

print('📝 Passo 5: Verificar status\n')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 6: Verificar logs\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -10')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Backend reconstruído!')

