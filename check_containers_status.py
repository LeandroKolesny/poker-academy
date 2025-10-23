#!/usr/bin/env python3
"""
Script para verificar o status dos containers
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

def check_status():
    """Verifica o status"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar containers
        print("1️⃣ Status dos containers...")
        cmd1 = "docker ps -a | grep poker"
        execute_command(client, cmd1)
        
        # Verificar logs do frontend
        print("\n2️⃣ Logs do frontend...")
        cmd2 = "docker logs poker_frontend | tail -50"
        execute_command(client, cmd2)
        
        # Verificar logs do backend
        print("\n3️⃣ Logs do backend...")
        cmd3 = "docker logs poker_backend | tail -20"
        execute_command(client, cmd3)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_status()

