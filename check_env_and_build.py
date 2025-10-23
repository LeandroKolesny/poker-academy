#!/usr/bin/env python3
"""
Script para verificar .env e fazer build
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
    """Check"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar .env
        print("📝 Verificando .env:")
        output, _ = execute_command(client, "ls -la /root/Dojo_Deploy/poker-academy/.env*")
        
        # Verificar conteúdo
        print("\n📝 Conteúdo do .env:")
        output, _ = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/.env.production")
        
        # Fazer build
        print("\n🔨 Fazendo build do backend...")
        output, _ = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build backend 2>&1 | tail -100")
        
        # Iniciar
        print("\n🚀 Iniciando containers...")
        output, _ = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d 2>&1")
        time.sleep(15)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, _ = execute_command(client, "docker ps")
        
        # Verificar logs do backend
        print("\n📝 Logs do backend:")
        output, _ = execute_command(client, "docker logs poker_backend --tail 50")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

