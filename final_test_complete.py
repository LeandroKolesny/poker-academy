#!/usr/bin/env python3
import paramiko
import time

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('✅ TESTE FINAL COMPLETO\n')
print('='*60)

print('\n📝 1. Verificar se o arquivo anterior ainda está no banco\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, student_id, month, year, file_size FROM student_database ORDER BY id DESC LIMIT 2;"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

print('\n📝 2. Verificar se os arquivos estão no container\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_backend ls -lh /app/uploads/databases/')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 3. Verificar se o frontend está respondendo\n')
stdin, stdout, stderr = client.exec_command('curl -s -I https://cardroomgrinders.com.br/ 2>&1 | head -5')
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 4. Verificar logs recentes do backend\n')
stdin, stdout, stderr = client.exec_command('docker logs poker_backend 2>&1 | tail -10')
output = stdout.read().decode('utf-8')
print(output)

print('\n' + '='*60)
print('✅ Teste concluído!')
print('\n🎯 PRÓXIMO PASSO: Faça login em https://cardroomgrinders.com.br')
print('   e teste o upload de um novo arquivo .zip!')

client.close()

