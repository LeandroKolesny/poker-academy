#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Copiando arquivo database_routes.py para o servidor...\n')

# Usar SFTP para copiar o arquivo
sftp = client.open_sftp()
local_file = 'poker-academy-backend/poker_academy_api/src/routes/database_routes.py'
remote_file = '/root/Dojo_Deploy/poker-academy/poker-academy-backend/poker_academy_api/src/routes/database_routes.py'

sftp.put(local_file, remote_file)
sftp.close()

print('✅ Arquivo copiado com sucesso!\n')

print('🔨 Rebuilding backend...\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose build backend --no-cache 2>&1 | tail -50')
output = stdout.read().decode('utf-8')
print(output)

print('\n⏳ Aguardando 5 segundos...')
time.sleep(5)

print('\n🚀 Reiniciando containers...\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d')
output = stdout.read().decode('utf-8')
print(output)

print('\n⏳ Aguardando 10 segundos para containers estabilizarem...')
time.sleep(10)

print('\n🐳 Status dos containers:\n')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Deploy concluído!')

