#!/usr/bin/env python3
"""
Script para debug detalhado
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

def debug():
    """Debug detalhado"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar se há Dockerfile
        print("📋 Verificando Dockerfile do frontend...")
        output, error = execute_command(client, "ls -la /root/Dojo_Deploy/poker-academy/")
        print(output)
        
        # Verificar se há Dockerfile
        print("\n📋 Procurando Dockerfile...")
        output, error = execute_command(client, "find /root/Dojo_Deploy/poker-academy -name 'Dockerfile*' -type f")
        print(output)
        
        # Verificar estrutura
        print("\n📋 Estrutura de poker-academy:")
        output, error = execute_command(client, "ls -la /root/Dojo_Deploy/poker-academy/poker-academy/")
        print(output)
        
        # Tentar iniciar manualmente
        print("\n📝 Tentando iniciar containers manualmente...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d 2>&1", timeout=120)
        print(output)
        if error:
            print("Erro:", error)
        
        # Aguardar
        time.sleep(10)
        
        # Verificar status
        print("\n📋 Status dos containers:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar logs
        print("\n📋 Logs do docker-compose:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -100")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug()

