#!/usr/bin/env python3
"""
Script para verificar status do frontend
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
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    
    return output, error

def check_status():
    """Verifica status do frontend"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar containers
        print("📝 Status dos containers:")
        output, _ = execute_command(client, "docker ps --format 'table {{.Names}}\t{{.Status}}'")
        print(output)
        
        # Verificar logs do frontend
        print("\n📝 Últimos logs do frontend:")
        output, _ = execute_command(client, "docker logs poker_frontend 2>&1 | tail -20")
        print(output)
        
        # Testar acesso
        print("\n📝 Testando acesso ao frontend...")
        output, _ = execute_command(client, "curl -s -o /dev/null -w 'Status: %{http_code}\\n' https://cardroomgrinders.com.br/admin/classes")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_status()

