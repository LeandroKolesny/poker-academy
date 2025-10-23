#!/usr/bin/env python3
"""
Script para iniciar frontend com detalhes
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

def start():
    """Inicia"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Remover container
        print("📝 Removendo container frontend...")
        execute_command(client, "docker rm -f poker_frontend")
        print("✅ Removido!\n")
        
        # Iniciar frontend
        print("📝 Iniciando frontend com docker-compose...")
        output, error = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d frontend 2>&1")
        print(output)
        print(error)
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 30 segundos...")
        time.sleep(30)
        
        # Verificar status
        print("\n📝 Status:")
        output, error = execute_command(client, "docker ps -a | grep frontend")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do frontend:")
        output, error = execute_command(client, "docker logs poker_frontend 2>&1")
        print(output)
        
        # Tentar iniciar manualmente
        print("\n📝 Tentando iniciar manualmente...")
        output, error = execute_command(client, "docker start poker_frontend 2>&1")
        print(output)
        print(error)
        
        # Aguardar
        print("\n⏳ Aguardando 10 segundos...")
        time.sleep(10)
        
        # Verificar status novamente
        print("\n📝 Status após iniciar:")
        output, error = execute_command(client, "docker ps -a | grep frontend")
        print(output)
        
        # Verificar logs novamente
        print("\n📝 Logs após iniciar:")
        output, error = execute_command(client, "docker logs poker_frontend 2>&1 | tail -50")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start()

