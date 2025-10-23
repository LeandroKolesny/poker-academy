#!/usr/bin/env python3
"""
Script para verificar estrutura do servidor
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

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar estrutura
        print("📝 Estrutura de /root/Dojo_Deploy/poker-academy:")
        output, error = execute_command(client, "ls -la /root/Dojo_Deploy/poker-academy/")
        print(output)
        
        # Verificar Dockerfile
        print("\n📝 Dockerfile do frontend:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/poker-academy/Dockerfile")
        print(output)
        
        # Verificar docker-compose
        print("\n📝 docker-compose.yml:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/docker-compose.yml | grep -A 20 'frontend:'")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

