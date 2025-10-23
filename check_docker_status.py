#!/usr/bin/env python3
"""
Script para verificar status do Docker
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
        
        # Verificar imagens
        print("📝 Imagens disponíveis:")
        output, error = execute_command(client, "docker images")
        print(output)
        
        # Verificar containers
        print("\n📝 Containers (todos):")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar docker-compose.yml
        print("\n📝 Conteúdo do docker-compose.yml:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/docker-compose.yml")
        print(output)
        
        # Tentar iniciar com verbose
        print("\n📝 Tentando iniciar com verbose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d 2>&1")
        print(output)
        print(error)
        
        # Aguardar
        time.sleep(60)
        
        # Verificar status novamente
        print("\n📝 Status após iniciar:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

