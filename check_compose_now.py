#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificando docker-compose.yml\n')
stdin, stdout, stderr = client.exec_command('cat /root/Dojo_Deploy/poker-academy/docker-compose.yml | grep -A 20 "frontend:"')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Tentando iniciar frontend com verbose\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up frontend 2>&1 | head -50')
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')
print(output)
if error:
    print(f"Erro: {error}")

client.close()

