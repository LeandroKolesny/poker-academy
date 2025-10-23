#!/usr/bin/env python3
"""
Script para debugar backend
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
    
    output = stdout.read().decode('utf-8', errors='replace')
    error = stderr.read().decode('utf-8', errors='replace')
    
    if output:
        print(output[-2000:] if len(output) > 2000 else output)
    
    return output, error

def debug():
    """Debug"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Listar containers
        print("📝 Containers em execução:")
        output, _ = execute_command(client, "docker ps")
        
        # Verificar logs do backend
        print("\n📝 Logs do backend (últimas 50 linhas):")
        output, _ = execute_command(client, "docker logs poker_backend --tail 50")
        
        # Verificar se há erros
        print("\n📝 Verificando erros no backend:")
        output, _ = execute_command(client, "docker logs poker_backend 2>&1 | grep -i error | tail -10")
        
        # Tentar reiniciar
        print("\n🔄 Tentando reiniciar backend...")
        output, _ = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose restart poker_backend")
        time.sleep(10)
        
        # Verificar status novamente
        print("\n📝 Status após restart:")
        output, _ = execute_command(client, "docker ps | grep poker")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug()

