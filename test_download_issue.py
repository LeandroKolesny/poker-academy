#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🔍 INVESTIGANDO ERRO 404 NO DOWNLOAD\n')
print('='*60)

print('\n📝 1. Verificar arquivos no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lh /app/uploads/databases/')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 2. Verificar registros no banco de dados\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, student_id, month, year, file_url, file_size FROM student_database;"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

print('\n📝 3. Testar rota de download com curl (sem autenticação)\n')
stdin, stdout, stderr = client.exec_command('curl -v https://cardroomgrinders.com.br/api/uploads/databases/db_26_jan_2025_ce71066c.zip 2>&1 | head -20')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 4. Verificar logs do backend para erros\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | grep -i "download\|404" | tail -10')
output = stdout.read().decode('utf-8')
print(output)

print('\n' + '='*60)

client.close()

