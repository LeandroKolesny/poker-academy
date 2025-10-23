#!/usr/bin/env python3
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('🔄 Reiniciando containers...\n')

stdin, stdout, stderr = client.exec_command('cd /root/Dojo_Deploy/poker-academy && docker-compose up -d')
output = stdout.read().decode('utf-8')
print(output)

print('\n⏳ Aguardando 10 segundos...')
time.sleep(10)

print('\n🐳 Status dos containers:\n')
stdin, stdout, stderr = client.exec_command('docker ps')
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Concluído!')

