#!/usr/bin/env python3
"""
Script para verificar se a tabela user_progress existe
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

def verify():
    """Verify"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar se a tabela existe
        print("1️⃣ Verificando se a tabela user_progress existe...")
        cmd = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW TABLES LIKE 'user_progress';" """
        execute_command(client, cmd)
        
        # Descrever a tabela
        print("\n2️⃣ Descrevendo a tabela user_progress...")
        cmd = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "DESCRIBE user_progress;" """
        execute_command(client, cmd)
        
        # Listar todas as tabelas
        print("\n3️⃣ Listando todas as tabelas...")
        cmd = """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SHOW TABLES;" """
        execute_command(client, cmd)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()

