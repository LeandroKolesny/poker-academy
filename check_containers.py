#!/usr/bin/env python3
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('🐳 Status dos containers:\n')
stdin, stdout, stderr = client.exec_command('docker ps -a')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Logs do docker-compose:\n')
stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose logs --tail=50')
output = stdout.read().decode('utf-8')
print(output)

client.close()

