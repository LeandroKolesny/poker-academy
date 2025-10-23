#!/usr/bin/env python3
"""
Script para verificar tipo de usuários
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

def check_users():
    """Verifica tipo de usuários"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar estrutura da tabela
        print("📝 Estrutura da tabela users:")
        output, _ = execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "DESCRIBE users;" """)
        
        # Verificar valores de type
        print("\n📝 Valores únicos de type:")
        output, _ = execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT DISTINCT type, COUNT(*) FROM users GROUP BY type;" """)
        
        # Verificar HEX dos valores
        print("\n📝 HEX dos valores de type:")
        output, _ = execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, name, type, HEX(type) FROM users LIMIT 5;" """)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_users()

