#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🔍 DEBUG: Verificar arquivo no servidor\n')

print('📝 1. Listar arquivos\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lh /app/uploads/databases/')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 2. Verificar registros no banco\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, student_id, month, year, file_url FROM student_database WHERE month=\'mar\';"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

print('\n📝 3. Testar rota pública (sem autenticação)\n')
stdin, stdout, stderr = client.exec_command('curl -s -I https://cardroomgrinders.com.br/api/uploads/databases/db_26_mar_2025_c6862a5b.zip 2>&1 | head -5')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 4. Verificar logs do backend\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -20')
output = stdout.read().decode('utf-8')
print(output)

client.close()

