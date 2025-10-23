#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('✅ VERIFICAÇÃO FINAL DO UPLOAD\n')
print('='*60)

print('\n📝 1. Arquivo no container:\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lh /app/uploads/databases/db_26_jan_2025_09ad111a.zip')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 2. Registro no banco de dados:\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT * FROM student_database WHERE id=1\\G"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

print('\n📝 3. Testando acesso ao arquivo via backend:\n')
stdin, stdout, stderr = client.exec_command('curl -s -I http://localhost:5000/api/uploads/databases/db_26_jan_2025_09ad111a.zip 2>&1 | head -10')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 4. Logs recentes do backend:\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -5')
output = stdout.read().decode('utf-8')
print(output)

client.close()

print('\n' + '='*60)
print('✅ Verificação concluída!')

