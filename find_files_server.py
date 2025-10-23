#!/usr/bin/env python3
"""
Script para encontrar arquivos no servidor
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

def find_files():
    """Encontra arquivos"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar ClassManagement.js
        print("📋 Procurando ClassManagement.js...")
        output, error = execute_command(client, "find /root/Dojo_Deploy -name 'ClassManagement.js' -type f")
        print(output)
        
        # Procurar Catalog.js
        print("\n📋 Procurando Catalog.js...")
        output, error = execute_command(client, "find /root/Dojo_Deploy -name 'Catalog.js' -type f")
        print(output)
        
        # Procurar History.js
        print("\n📋 Procurando History.js...")
        output, error = execute_command(client, "find /root/Dojo_Deploy -name 'History.js' -type f")
        print(output)
        
        # Procurar class_routes.py
        print("\n📋 Procurando class_routes.py...")
        output, error = execute_command(client, "find /root/Dojo_Deploy -name 'class_routes.py' -type f")
        print(output)
        
        # Procurar models.py
        print("\n📋 Procurando models.py...")
        output, error = execute_command(client, "find /root/Dojo_Deploy -name 'models.py' -type f")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_files()

