#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🔨 REBUILD SEM CACHE\n')

print('📝 Passo 1: Remover container\n')
stdin, stdout, stderr = client.exec_command('docker rm -f poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 2: Remover imagem\n')
stdin, stdout, stderr = client.exec_command('docker rmi poker-academy_backend')
output = stdout.read().decode('utf-8')
print(output)

print('📝 Passo 3: Rebuild sem cache\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache backend')
output = stdout.read().decode('utf-8')
print(output[-1000:])  # Últimas 1000 caracteres

print('\n📝 Passo 4: Iniciar backend\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 5: Aguardar 15 segundos\n')
time.sleep(15)

print('📝 Passo 6: Verificar arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep -n "send_from_directory" /app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
if output.strip():
    print(f"❌ Ainda tem send_from_directory:\n{output}")
else:
    print("✅ send_from_directory removido!")

print('\n📝 Passo 7: Verificar se send_file está importado\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep "send_file" /app/src/routes/database_routes.py | head -1')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Rebuild concluído!')

