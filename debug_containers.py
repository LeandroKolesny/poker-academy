#!/usr/bin/env python3
"""
Script para debugar containers
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

def debug_containers():
    """Debug dos containers"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar containers
        print("📋 Containers em execução:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar imagens
        print("\n📋 Imagens disponíveis:")
        output, error = execute_command(client, "docker images | grep poker")
        print(output)
        
        # Verificar docker-compose.yml
        print("\n📋 Conteúdo do docker-compose.yml:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/docker-compose.yml")
        print(output[:1000])
        
        # Tentar iniciar containers
        print("\n📝 Tentando iniciar containers...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose up -d 2>&1")
        print(output)
        if error:
            print("Erro:", error)
        
        # Aguardar
        time.sleep(10)
        
        # Verificar status
        print("\n📋 Status dos containers após iniciar:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar logs
        print("\n📋 Logs do docker-compose:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy && docker-compose logs 2>&1 | tail -50")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_containers()

