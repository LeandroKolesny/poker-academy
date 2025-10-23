#!/usr/bin/env python3
"""
Script para verificar erro do backend
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
    time.sleep(2)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    
    return output, error

def check_error():
    """Verifica erro"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Ver todos os logs
        print("📝 TODOS OS LOGS DO BACKEND:")
        output, _ = execute_command(client, "docker logs poker_backend 2>&1 | grep -A 5 'ERROR\\|Traceback\\|Exception' | head -100")
        print(output)
        
        # Tentar reiniciar
        print("\n🔄 Reiniciando backend...")
        execute_command(client, "docker restart poker_backend")
        time.sleep(10)
        
        # Verificar status
        print("\n📝 Status após restart:")
        output, _ = execute_command(client, "docker ps | grep poker_backend")
        print(output)
        
        # Ver logs novamente
        print("\n📝 Logs após restart:")
        output, _ = execute_command(client, "docker logs poker_backend 2>&1 | tail -50")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_error()

