#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🚀 DEPLOY: LAZY CLEANUP (5 MINUTOS)\n')

print('📝 Passo 1: Copiar arquivo atualizado\n')
sftp = client.open_sftp()
sftp.put(
    'poker-academy-backend/poker_academy_api/src/routes/database_routes.py',
    '/root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py'
)
print('✅ Arquivo copiado para poker-academy')
sftp.close()

print('\n📝 Passo 2: Copiar arquivo para o container\n')
stdin, stdout, stderr = client.exec_command(
    'docker cp /root/Dojo_Deploy/poker-academy/poker_academy_api/src/routes/database_routes.py poker_backend:/app/src/routes/database_routes.py'
)
output = stdout.read().decode('utf-8')
print('✅ Arquivo copiado para o container')

print('\n📝 Passo 3: Reiniciar backend\n')
stdin, stdout, stderr = client.exec_command('docker restart poker_backend')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 4: Aguardar 10 segundos\n')
time.sleep(10)

print('📝 Passo 5: Verificar arquivo no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend grep -n "cleanup_expired_databases" /app/src/routes/database_routes.py | head -1')
output = stdout.read().decode('utf-8')
print(f"✅ Função encontrada: {output.strip()}")

client.close()
print('\n✅ Deploy concluído!')

