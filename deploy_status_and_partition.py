#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🚀 DEPLOY: STATUS E FILTRO DE PARTIÇÃO\n')

print('📝 Passo 1: Copiar arquivos do backend\n')
sftp = client.open_sftp()
sftp.put(
    'poker-academy-backend/poker_academy_api/src/models.py',
    '/root/Dojo_Deploy/poker-academy/poker_academy_api/src/models.py'
)
print('✅ models.py copiado')

sftp.put(
    'poker-academy-backend/poker_academy_api/src/routes/database_routes.py',
    '/root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py'
)
print('✅ database_routes.py copiado')
sftp.close()

print('\n📝 Passo 2: Copiar arquivos para o container\n')
stdin, stdout, stderr = client.exec_command(
    'docker cp /root/Dojo_Deploy/poker-academy/poker_academy_api/src/models.py poker_backend:/app/src/models.py'
)
print('✅ models.py copiado para container')

stdin, stdout, stderr = client.exec_command(
    'docker cp /root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py poker_backend:/app/src/routes/database_routes.py'
)
print('✅ database_routes.py copiado para container')

print('\n📝 Passo 3: Reiniciar backend\n')
stdin, stdout, stderr = client.exec_command('docker restart poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 4: Aguardar 10 segundos\n')
time.sleep(10)

print('📝 Passo 5: Copiar arquivos do frontend\n')
sftp = client.open_sftp()
sftp.put(
    'poker-academy/src/components/admin/AdminMonthlyDatabase.js',
    '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminMonthlyDatabase.js'
)
print('✅ AdminMonthlyDatabase.js copiado')

sftp.put(
    'poker-academy/src/components/student/MonthlyDatabase.js',
    '/root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/MonthlyDatabase.js'
)
print('✅ MonthlyDatabase.js copiado')
sftp.close()

print('\n📝 Passo 6: Rebuild frontend\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build frontend')
output = stdout.read().decode('utf-8')
print('✅ Frontend rebuild iniciado')

print('\n📝 Passo 7: Aguardar 30 segundos\n')
time.sleep(30)

print('✅ Deploy concluído!')
client.close()

