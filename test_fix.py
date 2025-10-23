#!/usr/bin/env python3
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

# Verificar containers
print('📊 Containers em execução:')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

# Verificar logs recentes
print('\n📋 Últimos 20 logs do frontend:')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose logs frontend 2>&1 | tail -20')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Concluído!')

