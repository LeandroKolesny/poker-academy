#!/usr/bin/env python3
"""
Script para verificar build do Docker
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
        print(output[-2000:] if len(output) > 2000 else output)
    
    return output, error

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar estrutura de diretórios
        print("📁 Estrutura de diretórios:")
        output, _ = execute_command(client, "ls -la /root/Dojo_Deploy/poker-academy/poker-academy/ | grep -E 'build|src|public'")
        
        # Verificar se existe Dockerfile
        print("\n📝 Verificando Dockerfile:")
        output, _ = execute_command(client, "ls -la /root/Dojo_Deploy/poker-academy/ | grep -i docker")
        
        # Verificar conteúdo do docker-compose
        print("\n📝 Verificando docker-compose.yml:")
        output, _ = execute_command(client, "grep -A 10 'frontend:' /root/Dojo_Deploy/poker-academy/docker-compose.yml")
        
        # Verificar volumes
        print("\n📝 Verificando volumes do frontend:")
        output, _ = execute_command(client, "docker inspect poker_frontend | grep -A 20 'Mounts'")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

