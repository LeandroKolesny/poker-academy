#!/usr/bin/env python3
"""
Script para verificar arquivo de criação de usuários
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
        print(output[-3000:] if len(output) > 3000 else output)
    
    return output, error

def check_create_users():
    """Verifica arquivo de criação de usuários"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar arquivo de criação de usuários
        print("📝 Procurando arquivo de criação de usuários:")
        output, _ = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/create_admin_users.sql | head -50")
        
        print("\n📝 Verificando arquivo create_test_users.sql:")
        output, _ = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/create_test_users.sql | head -100")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_create_users()

