#!/usr/bin/env python3
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

# Verificar conteúdo do arquivo
print('📝 Conteúdo do StudentPanel.js no servidor:')
stdin, stdout, stderr = client.exec_command('cat /root/Dojo_Deploy/poker-academy/poker-academy/src/components/student/StudentPanel.js | grep -A 2 "Route index"')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Conteúdo do AdminPanel.js no servidor:')
stdin, stdout, stderr = client.exec_command('cat /root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/AdminPanel.js | grep -A 2 "Route index"')
output = stdout.read().decode('utf-8')
print(output)

client.close()

