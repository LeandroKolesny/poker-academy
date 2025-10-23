#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Passo 1: Copiar arquivos corrigidos para o servidor\n')

# Copiar MonthlyDatabase.js
sftp = client.open_sftp()
sftp.put('poker-academy/src/components/student/MonthlyDatabase.js', 
         '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/MonthlyDatabase.js')
print('✅ MonthlyDatabase.js copiado')

# Copiar AdminMonthlyDatabase.js
sftp.put('poker-academy/src/components/admin/AdminMonthlyDatabase.js',
         '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminMonthlyDatabase.js')
print('✅ AdminMonthlyDatabase.js copiado')
sftp.close()

print('\n📝 Passo 2: Rebuildar frontend\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build frontend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 3: Aguardar rebuild (30 segundos)\n')
time.sleep(30)

print('📝 Passo 4: Verificar logs do frontend\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_frontend 2>&1 | tail -20')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Deploy concluído!')

