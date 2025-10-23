#!/usr/bin/env python3
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('📝 Testando endpoint de download:\n')
stdin, stdout, stderr = client.exec_command('curl -s -I http://localhost:5000/uploads/databases/db_26_jan_2025_09ad111a.zip')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Testando com token:\n')
stdin, stdout, stderr = client.exec_command('curl -s -I -H "Authorization: Bearer test" http://localhost:5000/api/student/database/download/db_26_jan_2025_09ad111a.zip')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Verificando logs do backend:\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -20')
output = stdout.read().decode('utf-8')
print(output)

client.close()

