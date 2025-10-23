#!/usr/bin/env python3
"""
Script para encontrar DATABASE_URL
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

def find():
    """Encontra"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar DATABASE_URL em arquivos
        print("📝 Procurando DATABASE_URL em arquivos...")
        output, error = execute_command(client, "grep -r 'DATABASE_URL' /root/Dojo_Deploy/poker-academy/ 2>/dev/null | head -20")
        print(output)
        
        # Procurar em .env
        print("\n📝 Procurando .env files...")
        output, error = execute_command(client, "find /root/Dojo_Deploy/poker-academy/ -name '.env*' 2>/dev/null")
        print(output)
        
        # Verificar Dockerfile
        print("\n📝 Verificando Dockerfile do backend...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/poker-academy-backend/Dockerfile | grep -A5 -B5 'DATABASE_URL'")
        print(output if output else "Não encontrado")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find()

