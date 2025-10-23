#!/usr/bin/env python3
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('📝 Verificando volumes Docker:\n')
stdin, stdout, stderr = client.exec_command('docker volume ls')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Inspecionando volume backend_uploads:\n')
stdin, stdout, stderr = client.exec_command('docker volume inspect backend_uploads')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Conteúdo do volume:\n')
stdin, stdout, stderr = client.exec_command('docker run --rm -v backend_uploads:/data alpine ls -lah /data/')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Procurando por arquivos .zip no volume:\n')
stdin, stdout, stderr = client.exec_command('docker run --rm -v backend_uploads:/data alpine find /data -name "*.zip" 2>/dev/null')
output = stdout.read().decode('utf-8')
print(output)

client.close()

