#!/usr/bin/env python3
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('📝 Verificando StudentPanel.js no servidor:\n')
stdin, stdout, stderr = client.exec_command('cat /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js | head -40')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Procurando por "to=" em StudentPanel.js:\n')
stdin, stdout, stderr = client.exec_command('grep "to=" /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js')
output = stdout.read().decode('utf-8')
print(output)

client.close()

