#!/usr/bin/env python3
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('📝 Logs do backend (últimas 50 linhas):\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -50')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Procurando por "database/upload" nos logs:\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | grep -i "database/upload"')
output = stdout.read().decode('utf-8')
if output.strip():
    print(output)
else:
    print('❌ Nenhuma requisição de upload encontrada nos logs')

print('\n\n📝 Procurando por "POST" nos logs:\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | grep "POST" | tail -10')
output = stdout.read().decode('utf-8')
print(output)

client.close()

