#!/usr/bin/env python3
"""
Script para verificar se uploads foi removido
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
        
        # Verificar estrutura
        print("📝 Estrutura do poker_academy_api:")
        output, error = execute_command(client, "ls -la /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/")
        print(output)
        
        # Procurar por uploads
        print("\n📝 Procurando por diretório uploads...")
        output, error = execute_command(client, "find /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/ -name uploads -type d")
        if output.strip():
            print("❌ ENCONTRADO:")
            print(output)
        else:
            print("✅ Não encontrado")
        
        # Procurar por videos
        print("\n📝 Procurando por diretório videos...")
        output, error = execute_command(client, "find /root/Dojo_Deploy/poker-academy-backend/poker_academy_api/ -name videos -type d")
        if output.strip():
            print("❌ ENCONTRADO:")
            print(output)
        else:
            print("✅ Não encontrado")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()
