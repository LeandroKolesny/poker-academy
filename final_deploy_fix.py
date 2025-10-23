#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🔨 DEPLOY FINAL\n')

print('📝 Passo 1: Copiar arquivo\n')
sftp = client.open_sftp()
sftp.put('poker-academy-backend/poker_academy_api/src/routes/database_routes.py',
         '/root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
print('✅ Arquivo copiado')
sftp.close()

print('\n📝 Passo 2: Parar containers\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose down')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 3: Remover imagens\n')
stdin, stdout, stderr = client.exec_command('docker rmi poker-academy_backend poker-academy_frontend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 4: Rebuild completo\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build')
output = stdout.read().decode('utf-8')
print(output[-1500:])

print('\n📝 Passo 5: Aguardar 20 segundos\n')
time.sleep(20)

print('📝 Passo 6: Verificar status\n')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 7: Verificar arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep "send_file" /app/src/routes/database_routes.py | head -1')
output = stdout.read().decode('utf-8')
print(f"send_file import: {output}")

client.close()
print('\n✅ Deploy concluído!')

