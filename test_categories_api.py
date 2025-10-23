#!/usr/bin/env python3
"""
Script para testar categorias via API
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
        
        # Verificar se o backend está respondendo
        print("📝 Testando backend com wget...")
        output, error = execute_command(client, "docker exec poker_backend wget -q -O - http://localhost:5000/api/health 2>&1 || echo 'Erro'")
        print(output)
        
        # Verificar logs do backend
        print("\n📝 Últimos logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -20")
        print(output)
        
        # Tentar acessar a API de classes
        print("\n📝 Testando API de classes...")
        output, error = execute_command(client, "docker exec poker_backend wget -q -O - http://localhost:5000/api/classes 2>&1 | head -50")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()

