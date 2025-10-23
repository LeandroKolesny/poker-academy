#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('🚀 MIGRAÇÃO: ADICIONAR CAMPO STATUS\n')

print('📝 Passo 1: Adicionar coluna status\n')

sql_command = """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
ALTER TABLE student_database 
ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'ativo' AFTER file_size;
"
"""

stdin, stdout, stderr = client.exec_command(sql_command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

if error:
    print(f'⚠️ Aviso: {error}')
else:
    print('✅ Coluna status adicionada')

print('\n📝 Passo 2: Verificar schema\n')

sql_command = """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
DESCRIBE student_database;
"
"""

stdin, stdout, stderr = client.exec_command(sql_command)
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Passo 3: Verificar registros\n')

sql_command = """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
SELECT id, student_id, month, year, status FROM student_database LIMIT 5;
"
"""

stdin, stdout, stderr = client.exec_command(sql_command)
output = stdout.read().decode('utf-8')
print(output)

client.close()
print('\n✅ Migração concluída!')

