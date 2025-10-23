#!/usr/bin/env python3
"""
Script para resolver conflito de porta
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

def fix():
    """Corrige"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar qual processo está usando porta 80
        print("📝 Verificando qual processo está usando porta 80...")
        output, error = execute_command(client, "netstat -tlnp | grep :80")
        print(output)
        
        # Verificar todos os containers
        print("\n📝 Todos os containers:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Remover container frontend
        print("\n📝 Removendo container frontend...")
        execute_command(client, "docker rm -f poker_frontend")
        print("✅ Removido!\n")
        
        # Verificar novamente
        print("📝 Verificando porta 80 novamente...")
        output, error = execute_command(client, "netstat -tlnp | grep :80")
        print(output)
        
        # Iniciar frontend
        print("\n📝 Iniciando frontend...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d frontend 2>&1")
        print(output)
        
        # Aguardar
        print("\n⏳ Aguardando 30 segundos...")
        time.sleep(30)
        
        # Verificar status
        print("\n📝 Status:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do frontend:")
        output, error = execute_command(client, "docker logs poker_frontend 2>&1 | tail -50")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix()

