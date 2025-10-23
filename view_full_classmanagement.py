#!/usr/bin/env python3
"""
Script para visualizar ClassManagement.js completo
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command):
    """Executa um comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def view():
    """Visualiza"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        file_path = "/root/Dojo_Deploy/poker-academy/poker-academy/src/components/admin/ClassManagement.js"
        
        # Ver tamanho do arquivo
        print("📋 Informações do arquivo:")
        output, error = execute_command(client, f"wc -l {file_path}")
        print(output)
        
        # Ver primeiras 50 linhas
        print("\n📋 Primeiras 50 linhas:")
        output, error = execute_command(client, f"head -50 {file_path}")
        print(output)
        
        # Procurar por 'category'
        print("\n📋 Linhas com 'category':")
        output, error = execute_command(client, f"grep -n 'category' {file_path}")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    view()

