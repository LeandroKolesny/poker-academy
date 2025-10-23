#!/usr/bin/env python3
"""
Script para verificar encoding do banco de dados
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
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    
    return output, error

def check_encoding():
    """Verifica encoding do banco de dados"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar charset da tabela
        print("📝 Verificando charset da tabela classes:")
        output, _ = execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW CREATE TABLE classes\\G" """)
        print(output)
        
        # Verificar dados na tabela
        print("\n📝 Verificando dados na tabela classes:")
        output, _ = execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, name, HEX(name) FROM classes LIMIT 3;" """)
        print(output)
        
        # Verificar charset do banco
        print("\n📝 Verificando charset do banco:")
        output, _ = execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW CREATE DATABASE poker_academy\\G" """)
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_encoding()

