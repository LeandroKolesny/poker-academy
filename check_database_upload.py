#!/usr/bin/env python3
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('142.93.206.128', username='root', password='DojoShh159357')

print('📝 Verificando tabela student_database:\n')
stdin, stdout, stderr = client.exec_command('docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT * FROM student_database;"')
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

print('\n\n📝 Verificando arquivos salvos:\n')
stdin, stdout, stderr = client.exec_command('ls -lah /root/Dojo_Deploy/poker-academy/uploads/databases/ 2>/dev/null || echo "Diretório não encontrado"')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Procurando por diretórios de upload:\n')
stdin, stdout, stderr = client.exec_command('find /root/Dojo_Deploy -name "databases" -type d 2>/dev/null')
output = stdout.read().decode('utf-8')
print(output)

print('\n\n📝 Procurando por arquivos .zip:\n')
stdin, stdout, stderr = client.exec_command('find /root/Dojo_Deploy -name "*.zip" 2>/dev/null')
output = stdout.read().decode('utf-8')
print(output)

client.close()

