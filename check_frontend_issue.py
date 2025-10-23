#!/usr/bin/env python3
"""
Script para verificar o problema do frontend
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
        print(output)
    
    return output, error

def check():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar se o arquivo nginx.conf existe
        print("1️⃣ Verificando nginx.conf...")
        cmd1 = "ls -la /root/Dojo_Deploy/poker-academy/nginx.conf"
        execute_command(client, cmd1)
        
        # Verificar se o build do frontend existe
        print("\n2️⃣ Verificando build do frontend...")
        cmd2 = "ls -la /root/Dojo_Deploy/poker-academy/poker-academy/build/ | head -20"
        execute_command(client, cmd2)
        
        # Verificar logs completos do frontend
        print("\n3️⃣ Logs completos do frontend...")
        cmd3 = "docker logs poker_frontend 2>&1 | tail -100"
        execute_command(client, cmd3)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

