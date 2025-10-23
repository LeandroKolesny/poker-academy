#!/usr/bin/env python3
"""
Script para corrigir encoding dos dados usando CONVERT
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

def fix_encoding():
    """Corrige encoding dos dados usando CONVERT"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Corrigir encoding usando CONVERT
        print("📝 Corrigindo encoding dos dados...")
        
        # Converter name
        execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE classes SET name = CONVERT(CAST(CONVERT(name USING latin1) AS BINARY) USING utf8mb4);" """)
        
        # Converter description
        execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "UPDATE classes SET description = CONVERT(CAST(CONVERT(description USING latin1) AS BINARY) USING utf8mb4);" """)
        
        # Verificar dados corrigidos
        print("\n📝 Verificando dados corrigidos:")
        output, _ = execute_command(client, """docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e "SELECT id, name, HEX(name) FROM classes LIMIT 3;" """)
        print(output)
        
        print("\n✅ DADOS CORRIGIDOS COM SUCESSO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_encoding()

