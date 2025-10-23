#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Copiar arquivo com debug\n')
sftp = client.open_sftp()
sftp.put('poker-academy-backend/poker_academy_api/src/routes/database_routes.py',
         '/root/Dojo_Deploy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py')
print('✅ Arquivo copiado')
sftp.close()

print('\n📝 Remover container\n')
stdin, stdout, stderr = client.exec_command('docker rm -f poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Rebuildar\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d --build backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Aguardar 15 segundos\n')
time.sleep(15)

print('📝 Testar download\n')
stdin, stdout, stderr = client.exec_command('curl -s -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNiwidXNlcm5hbWUiOiJsZWFuZHJva29sZXMiLCJ0eXBlIjoic3R1ZGVudCIsImlhdCI6MTcyOTEzNzI2MCwiZXhwIjoxNzI5MjIzNjYwfQ.ch-95Y18Y01gvGn1f8d4PzzG6DyUjR-GkHDErQVsvbs" https://cardroomgrinders.com.br/api/student/database/download/db_26_jan_2025_59dd7852.zip -I 2>&1 | head -5')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar logs\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -20')
output = stdout.read().decode('utf-8')
print(output)

client.close()

