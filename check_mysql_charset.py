#!/usr/bin/env python3
"""
Script para verificar o charset do MySQL
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=120):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(1)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output)
    
    return output, error

def check_charset():
    """Verifica o charset"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar charset do banco
        print("1️⃣ Verificando charset do banco...")
        cmd1 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW CREATE DATABASE poker_academy;" """
        execute_command(client, cmd1)
        
        # Verificar charset da tabela
        print("\n2️⃣ Verificando charset da tabela...")
        cmd2 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW CREATE TABLE particoes;" """
        execute_command(client, cmd2)
        
        # Verificar charset da coluna
        print("\n3️⃣ Verificando charset da coluna...")
        cmd3 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW FULL COLUMNS FROM particoes;" """
        execute_command(client, cmd3)
        
        # Verificar variáveis de conexão
        print("\n4️⃣ Verificando variáveis de conexão...")
        cmd4 = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW VARIABLES LIKE 'character%';" """
        execute_command(client, cmd4)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_charset()

