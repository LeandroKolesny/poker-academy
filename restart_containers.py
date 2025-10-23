#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Reiniciando containers\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Aguardando 15 segundos para containers iniciarem...\n')
time.sleep(15)

print('📝 Verificando status\n')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificando logs do frontend\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_frontend 2>&1 | tail -10')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Containers reiniciados!')

