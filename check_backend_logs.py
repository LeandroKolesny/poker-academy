#!/usr/bin/env python3
"""
Script para verificar logs do backend
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
        
        # Verificar logs do backend
        print("📝 Logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -100")
        print(output)
        
        # Verificar se o backend está respondendo
        print("\n📝 Testando backend com curl...")
        output, error = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/health")
        print(output)
        print(error)
        
        # Verificar conexão com banco de dados
        print("\n📝 Testando conexão com banco de dados...")
        output, error = execute_command(client, "docker exec poker_mysql mysql -u poker_user -pDojo@Sql159357 poker_academy -e \"SELECT COUNT(*) FROM classes;\"")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

