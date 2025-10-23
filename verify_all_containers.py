#!/usr/bin/env python3
"""
Script para verificar todos os containers
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

def verify():
    """Verifica"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar status
        print("📝 Status dos containers:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar logs do frontend
        print("\n📝 Logs do frontend:")
        output, error = execute_command(client, "docker logs poker_frontend 2>&1 | tail -50")
        print(output)
        
        # Verificar logs do backend
        print("\n📝 Logs do backend:")
        output, error = execute_command(client, "docker logs poker_backend 2>&1 | tail -50")
        print(output)
        
        # Testar conexão com backend
        print("\n📝 Testando conexão com backend...")
        output, error = execute_command(client, "curl -s http://localhost:5000/api/health || echo 'Erro na conexão'")
        print(output)
        
        client.close()
        
        print("\n" + "=" * 70)
        print("✅ VERIFICAÇÃO CONCLUÍDA!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()

