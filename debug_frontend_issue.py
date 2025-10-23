#!/usr/bin/env python3
"""
Script para debugar problema do frontend
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

def debug():
    """Debuga"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Verificar todos os containers
        print("📝 Todos os containers:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar imagens
        print("\n📝 Imagens disponíveis:")
        output, error = execute_command(client, "docker images | grep poker")
        print(output)
        
        # Verificar redes
        print("\n📝 Redes:")
        output, error = execute_command(client, "docker network ls")
        print(output)
        
        # Tentar iniciar frontend com docker-compose
        print("\n📝 Iniciando frontend com docker-compose...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d frontend 2>&1")
        print("✅ Comando enviado!\n")
        
        # Aguardar
        print("⏳ Aguardando 30 segundos...")
        time.sleep(30)
        
        # Verificar status
        print("\n📝 Status:")
        output, error = execute_command(client, "docker ps -a")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do frontend:")
        output, error = execute_command(client, "docker logs poker_frontend 2>&1 | tail -100")
        print(output)
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug()

