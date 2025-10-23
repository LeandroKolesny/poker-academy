#!/usr/bin/env python3
"""
Script para verificar banco de dados
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=60):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def verify():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar status do MySQL
        print("📝 Status do MySQL:")
        output, error = execute_command(client, "docker ps | grep mysql")
        print(output)
        
        # Verificar logs do MySQL
        print("\n📝 Logs do MySQL:")
        output, error = execute_command(client, "docker logs poker_mysql 2>&1 | tail -50")
        print(output)
        
        # Tentar conectar ao MySQL
        print("\n📝 Testando conexão com MySQL...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e \"SELECT 1;\"", timeout=10)
        print(f"Output: {output}")
        print(f"Error: {error}")
        
        # Verificar se o banco de dados existe
        print("\n📝 Verificando bancos de dados...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u root -ppoker_academy_2025 -e \"SHOW DATABASES;\"", timeout=10)
        print(f"Output: {output}")
        print(f"Error: {error}")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()

