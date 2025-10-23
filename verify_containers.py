#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificando status dos containers\n')
stdin, stdout, stderr = client.exec_command('docker ps -a')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Aguardando 10 segundos para frontend iniciar...\n')
time.sleep(10)

print('📝 Verificando logs do frontend\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_frontend 2>&1 | tail -20')
output = stdout.read().decode('utf-8')
print(output)

client.close()

