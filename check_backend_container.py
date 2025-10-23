#!/usr/bin/env python3
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('📝 Verificando diretório /app/uploads dentro do container:\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lah /app/uploads/')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Procurando por diretório databases:\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lah /app/uploads/databases/ 2>/dev/null || echo "Diretório não existe"')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Procurando por arquivos .zip:\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend find /app/uploads -name "*.zip" 2>/dev/null')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Verificando permissões do diretório /app/uploads:\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend stat /app/uploads/')
output = stdout.read().decode('utf-8')
print(output)

client.close()

