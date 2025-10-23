#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🚀 DEPLOY: MONTHLY DATABASE ATUALIZADO\n')

print('📝 Passo 1: Copiar MonthlyDatabase.js\n')
sftp = client.open_sftp()
sftp.put(
    'poker-academy/src/components/student/MonthlyDatabase.js',
    '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/MonthlyDatabase.js'
)
print('✅ MonthlyDatabase.js copiado para servidor')
sftp.close()

print('\n📝 Passo 2: Rebuild frontend\n')
stdin, stdout, stderr = client.exec_command(
    'cd /root/Dojo_Deploy && docker-compose up -d --build poker_frontend'
)
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 3: Aguardar 15 segundos\n')
time.sleep(15)

print('📝 Passo 4: Verificar status\n')
stdin, stdout, stderr = client.exec_command('docker ps | grep poker_frontend')
output = stdout.read().decode('utf-8')
print(output)

print('\n✅ Deploy concluído!')
client.close()

