#!/usr/bin/env python3
"""
Script para verificar status do backend
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

def test():
    """Testa"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Status do container
        print("📝 Status do container backend:")
        output, error = execute_command(client, "docker ps | grep backend")
        print(output)
        
        # Health check
        print("\n📝 Health check:")
        output, error = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/health")
        print(f"Response: {output}")
        
        # Testar login
        print("\n📝 Testando login:")
        output, error = execute_command(client, "docker exec poker_backend curl -s -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
        print(f"Response: {output}")
        
        # Verificar logs
        print("\n📝 Logs do backend (últimas 30 linhas):")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -30")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

