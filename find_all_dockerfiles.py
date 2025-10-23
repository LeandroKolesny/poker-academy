#!/usr/bin/env python3
"""
Script para encontrar todos os Dockerfiles
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
        
        # Procurar por Dockerfiles
        print("📝 Procurando por Dockerfiles...")
        output, error = execute_command(client, "find /root/Dojo_Deploy -name 'Dockerfile*' -type f")
        print(output)
        
        # Verificar cada um
        dockerfiles = output.strip().split('\n')
        for dockerfile in dockerfiles:
            if dockerfile:
                print(f"\n📝 Conteúdo de {dockerfile}:")
                output, error = execute_command(client, f"grep -n 'mkdir' {dockerfile}")
                print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find()

