#!/usr/bin/env python3
"""
Script para verificação detalhada
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
        
        # Tentar build novamente com output completo
        print("\n📝 Tentando build novamente...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build 2>&1 | tail -200", timeout=600)
        print(output)
        
        # Verificar se há erro
        if "error" in output.lower() or "failed" in output.lower():
            print("\n❌ ERRO ENCONTRADO NO BUILD!")
        else:
            print("\n✅ Build parece OK")
        
        # Tentar iniciar
        print("\n📝 Tentando iniciar...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d 2>&1")
        print(output)
        
        time.sleep(60)
        
        # Verificar containers
        print("\n📝 Containers:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs:")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose logs 2>&1 | tail -200")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

