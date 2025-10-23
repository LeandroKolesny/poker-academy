#!/usr/bin/env python3
"""
Script para verificar configuração do docker-compose
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

def check_config():
    """Verifica configuração"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar docker-compose.yml
        print("📋 Conteúdo do docker-compose.yml:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/docker-compose.yml")
        print(output)
        
        # Verificar Dockerfile do frontend
        print("\n📋 Conteúdo do Dockerfile do frontend:")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/Dockerfile")
        print(output[:1000])
        
        # Tentar iniciar com logs
        print("\n📝 Tentando iniciar frontend com logs...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up frontend 2>&1 | head -50")
        print(output)
        if error:
            print("Erro:", error)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_config()

