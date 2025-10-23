#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🔨 REBUILD SEM CACHE - FINAL\n')

print('📝 Passo 1: Parar backend\n')
stdin, stdout, stderr = client.exec_command('docker stop poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 2: Remover container\n')
stdin, stdout, stderr = client.exec_command('docker rm poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 3: Remover imagem\n')
stdin, stdout, stderr = client.exec_command('docker rmi poker-academy_backend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 4: Rebuild sem cache\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker build --no-cache -t poker-academy_backend -f Dockerfile .')
output = stdout.read().decode('utf-8')
print(output[-1000:])

print('\n📝 Passo 5: Iniciar backend\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 6: Aguardar 15 segundos\n')
time.sleep(15)

print('📝 Passo 7: Verificar arquivo\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep "send_file" /app/src/routes/database_routes.py | head -1')
output = stdout.read().decode('utf-8')
print(f"send_file: {output}")

client.close()
print('\n✅ Rebuild concluído!')

