#!/usr/bin/env python3
"""
Script para fazer rebuild do backend usando docker-compose
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
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(output)
    if error and "DEPRECATED" not in error:
        print(f"❌ Erro: {error}")
    
    return output, error

def rebuild():
    """Faz rebuild do backend"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Ir para diretório
        print("📂 Entrando no diretório /root/Dojo_Deploy/poker-academy...")
        
        # Parar e remover containers
        print("🛑 Parando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose down")
        time.sleep(3)
        
        # Rebuild
        print("🔨 Fazendo rebuild...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose build --no-cache poker_backend", timeout=600)
        time.sleep(2)
        
        # Iniciar
        print("🚀 Iniciando containers...")
        execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(10)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, _ = execute_command(client, "docker ps --format 'table {{.Names}}\\t{{.Status}}'")
        
        # Testar endpoint
        print("\n📝 Testando endpoint /api/classes...")
        time.sleep(5)
        output, _ = execute_command(client, "docker exec poker_backend curl -s http://localhost:5000/api/test")
        print(output)
        
        # Verificar logs
        print("\n📝 Logs do backend (últimas 30 linhas):")
        output, _ = execute_command(client, "docker logs poker_backend 2>&1 | tail -30")
        print(output)
        
        client.close()
        print("\n✅ Rebuild concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild()

