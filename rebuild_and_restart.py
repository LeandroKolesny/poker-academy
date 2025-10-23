#!/usr/bin/env python3
"""
Script para fazer rebuild completo e reiniciar
"""

import paramiko
import time

SSH_HOST = "142.93.206.128"
SSH_USER = "root"
SSH_PASSWORD = "DojoShh159357"
SSH_PORT = 22

def execute_command(client, command, timeout=300):
    """Executa um comando via SSH"""
    print(f"\n📝 Executando: {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    time.sleep(2)
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output[-2000:] if len(output) > 2000 else output)
    
    return output, error

def rebuild():
    """Rebuild"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Parar todos os containers
        print("🛑 Parando todos os containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        time.sleep(5)
        
        # Remover imagem antiga
        print("\n🗑️  Removendo imagem antiga...")
        execute_command(client, "docker rmi poker-academy_backend:latest")
        
        # Fazer rebuild
        print("\n🔨 Fazendo rebuild...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache backend", timeout=600)
        
        # Iniciar
        print("\n🚀 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(20)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        execute_command(client, "docker ps")
        
        # Verificar logs
        print("\n📝 Logs do backend:")
        execute_command(client, "docker logs poker_backend --tail 50")
        
        print("\n✅ REBUILD COMPLETO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild()

