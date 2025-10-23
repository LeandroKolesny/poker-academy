#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar logs do backend\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -50')
output = stdout.read().decode('utf-8')
print(output)

client.close()

