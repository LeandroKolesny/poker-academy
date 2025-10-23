#!/usr/bin/env python3
"""
Script para verificar docker-compose e reconstruir frontend
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
        
        # Verificar docker-compose
        print("📝 Verificando docker-compose.yml...")
        output, error = execute_command(client, "cat /root/Dojo_Deploy/poker-academy/docker-compose.yml")
        print(output)
        
        # Remover frontend
        print("\n📝 Removendo container frontend...")
        execute_command(client, "docker rm -f poker_frontend")
        print("✅ Removido!\n")
        
        # Reconstruir frontend
        print("📝 Reconstruindo frontend...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build frontend --no-cache 2>&1 | tail -50", timeout=600)
        print(output)
        
        # Iniciar frontend
        print("\n📝 Iniciando frontend...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d frontend")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 60 segundos...")
        time.sleep(60)
        
        # Verificar status
        print("\n📝 Status:")
        output, error = execute_command(client, "docker ps")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()

