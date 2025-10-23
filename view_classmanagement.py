#!/usr/bin/env python3
"""
Script para visualizar ClassManagement.js
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
        
        # Procurar por select com name="category"
        print("📋 Procurando select com name='category'...")
        output, error = execute_command(client, f"grep -n -A 20 'name=\"category\"' {file_path} | head -30")
        print(output)
        
        # Procurar por getCategoryName
        print("\n📋 Procurando função getCategoryName...")
        output, error = execute_command(client, f"grep -n -A 10 'getCategoryName' {file_path} | head -20")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    view()

