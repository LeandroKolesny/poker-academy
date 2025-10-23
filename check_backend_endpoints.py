#!/usr/bin/env python3
"""
Script para verificar endpoints do backend
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
        
        # Verificar logs do backend
        print("📝 Logs do backend (últimas 100 linhas):")
        output, _ = execute_command(client, "docker logs poker_backend --tail 100")
        
        # Testar health
        print("\n🧪 Testando /api/health:")
        output, _ = execute_command(client, "curl -s http://localhost:5000/api/health")
        
        # Testar test
        print("\n🧪 Testando /api/test:")
        output, _ = execute_command(client, "curl -s http://localhost:5000/api/test")
        
        # Testar login
        print("\n🧪 Testando /api/login:")
        output, _ = execute_command(client, "curl -s -X POST http://localhost:5000/api/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

