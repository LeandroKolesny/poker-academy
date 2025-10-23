#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🚀 REINICIAR TODOS OS CONTAINERS\n')

print('📝 Passo 1: Parar todos os containers\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose down')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 2: Aguardar 5 segundos\n')
time.sleep(5)

print('📝 Passo 3: Iniciar todos os containers\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 4: Aguardar 30 segundos\n')
time.sleep(30)

print('📝 Passo 5: Verificar status\n')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Containers reiniciados!')

