#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Passo 1: Remover container antigo\n')
stdin, stdout, stderr = client.exec_command('docker rm -f 1378c71c14b1_poker_frontend 2>/dev/null || echo "Container não encontrado"')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 2: Remover imagem antiga\n')
stdin, stdout, stderr = client.exec_command('docker rmi 8c0911c64f1a 2>/dev/null || echo "Imagem não encontrada"')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 3: Iniciar frontend\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d frontend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 4: Aguardar 15 segundos\n')
time.sleep(15)

print('📝 Passo 5: Verificar status\n')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 6: Verificar logs\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_frontend 2>&1 | tail -15')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Frontend reiniciado!')

