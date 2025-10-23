#!/usr/bin/env python3
"""
Script para remover e reiniciar backend
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

def restart():
    """Restart"""
    
    try:
        print("🔌 Conectando ao servidor SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD, timeout=10)
        print("✅ Conectado ao servidor SSH!\n")
        
        # Remover container antigo
        print("🗑️  Removendo container antigo...")
        output, _ = execute_command(client, "docker rm -f poker_backend")
        
        # Iniciar
        print("\n🚀 Iniciando containers...")
        output, _ = execute_command(client, "cd /root/Dojo_Deploy/poker-academy && docker-compose up -d")
        time.sleep(15)
        
        # Verificar status
        print("\n📝 Status dos containers:")
        output, _ = execute_command(client, "docker ps")
        
        # Verificar logs do backend
        print("\n📝 Logs do backend:")
        output, _ = execute_command(client, "docker logs poker_backend --tail 50")
        
        # Testar health
        print("\n🧪 Testando health check:")
        output, _ = execute_command(client, "curl -s http://localhost:5000/api/health")
        
        print("\n✅ BACKEND INICIADO COM SUCESSO!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restart()

