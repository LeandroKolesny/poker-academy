#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Passo 1: Copiar arquivo diretamente para o container\n')
stdin, stdout, stderr = client.exec_command('docker cp /root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py poker_backend:/app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 2: Verificar arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend head -5 /app/src/routes/database_routes.py')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 3: Reiniciar backend\n')
stdin, stdout, stderr = client.exec_command('docker restart poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 4: Aguardar 10 segundos\n')
time.sleep(10)

print('📝 Passo 5: Testar download\n')
stdin, stdout, stderr = client.exec_command('curl -s -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNiwidXNlcm5hbWUiOiJsZWFuZHJva29sZXMiLCJ0eXBlIjoic3R1ZGVudCIsImV4cCI6MTcyOTEzNzI4MH0.ch-95Y18Y01gvGn1f8d4PzzG6DyUjR-GkHDErQVsvbs" http://localhost:5000/api/student/database/download/db_26_jan_2025_59dd7852.zip -o /tmp/test.zip && echo "✅ Download bem-sucedido" || echo "❌ Download falhou"')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Teste concluído!')

