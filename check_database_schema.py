#!/usr/bin/env python3
import paramiko

SSH_HOST = '142.93.206.128'
SSH_USER = 'root'
SSH_PASSWORD = 'DojoShh159357'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

print('📝 Verificar schema da tabela student_database\n')

sql_command = """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
DESCRIBE student_database;
"
"""

stdin, stdout, stderr = client.exec_command(sql_command)
output = stdout.read().decode('utf-8')
print(output)

print('\n📝 Verificar registros\n')

sql_command = """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "
SELECT id, student_id, month, year, status FROM student_database LIMIT 5;
"
"""

stdin, stdout, stderr = client.exec_command(sql_command)
output = stdout.read().decode('utf-8')
print(output)

client.close()

