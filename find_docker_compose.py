#!/usr/bin/env python3
"""
Script para encontrar docker-compose.yml
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

def find_docker_compose():
    """Encontra docker-compose.yml"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Procurar docker-compose.yml
        print("📋 Procurando docker-compose.yml...")
        output, error = execute_command(client, "find /root -name 'docker-compose.yml' -o -name 'docker-compose.yaml' 2>/dev/null")
        print(output)
        
        # Listar estrutura de /root/Dojo_Deploy
        print("\n📋 Estrutura de /root/Dojo_Deploy:")
        output, error = execute_command(client, "ls -la /root/Dojo_Deploy/")
        print(output)
        
        # Listar estrutura de /root
        print("\n📋 Estrutura de /root:")
        output, error = execute_command(client, "ls -la /root/")
        print(output)
        
        # Procurar por containers em execução
        print("\n📋 Containers em execução:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar como o backend está rodando
        print("\n📋 Inspecionando container backend:")
        output, error = execute_command(client, "docker inspect backend 2>&1 | grep -A 5 'Mounts\\|Env'")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_docker_compose()

