#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🚀 COPIAR MODELS.PY PARA CONTAINER\n')

print('📝 Passo 1: Copiar arquivo\n')
sftp = client.open_sftp()
sftp.put(
    'poker-academy-backend/poker_academy_api/src/models.py',
    '/root/Dojo_Deploy/poker-academy/poker_academy_api/src/models.py'
)
print('✅ models.py copiado para servidor')
sftp.close()

print('\n📝 Passo 2: Copiar para container\n')
stdin, stdout, stderr = client.exec_command(
    'docker cp /root/Dojo_Deploy/poker-academy/poker_academy_api/src/models.py poker_backend:/app/src/models.py'
)
print('✅ models.py copiado para container')

print('\n📝 Passo 3: Reiniciar backend\n')
stdin, stdout, stderr = client.exec_command('docker restart poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 4: Aguardar 10 segundos\n')
time.sleep(10)

print('✅ Concluído!')
client.close()

