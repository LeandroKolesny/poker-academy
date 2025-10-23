#!/usr/bin/env python3
"""
Script para verificar usuários no banco de dados
"""
import paramiko

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"

MYSQL_USER = "poker_user"
MYSQL_PASSWORD = "Dojo@Sql159357"
MYSQL_DATABASE = "poker_academy"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("🔌 Conectando ao servidor...")
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
    print("✅ Conectado!")
    
    # Verificar usuários
    print("\n📋 Usuários no banco de dados:")
    cmd = f"""docker exec poker_mysql mysql -u {MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE} -e "SELECT id, name, username, type FROM users LIMIT 10;" """
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    
    print(output)
    
finally:
    ssh.close()

