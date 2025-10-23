#!/usr/bin/env python3
"""
Script para verificar se a tabela student_database existe no banco
"""
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔌 Conectando ao servidor...")
client.connect('142.93.206.128', username='root', password='DojoShh159357')
print("✅ Conectado!")

# Verificar se a tabela existe
print("\n📋 Verificando tabelas no banco de dados...")
command = """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW TABLES LIKE 'student_database';"
"""

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(f"Output:\n{output}")
if error:
    print(f"Error:\n{error}")

# Listar todas as tabelas
print("\n📋 Todas as tabelas do banco:")
command = """
docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW TABLES;"
"""

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print(f"Output:\n{output}")
if error:
    print(f"Error:\n{error}")

# Verificar logs do backend
print("\n📝 Logs do backend (últimas 30 linhas):")
command = "docker logs poker_backend 2>&1 | tail -30"

stdin, stdout, stderr = client.exec_command(command)
output = stdout.read().decode('utf-8')

print(output)

client.close()
print("\n✅ Verificação concluída!")

