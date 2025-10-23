#!/usr/bin/env python3
"""
Script para verificar arquivos .env
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
        
        # Verificar .env no backend
        print("📝 Verificando .env no backend...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/poker-academy-backend/.env 2>&1 || echo 'Arquivo não encontrado'")
        print(output)
        
        # Verificar .env na raiz
        print("\n📝 Verificando .env na raiz...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/.env 2>&1 || echo 'Arquivo não encontrado'")
        print(output)
        
        # Verificar variáveis de ambiente do container
        print("\n📝 Variáveis de ambiente do backend:")
        output, error = execute_command(client, "docker exec poker_backend env | grep -E 'DB_|FLASK_|DATABASE'")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

